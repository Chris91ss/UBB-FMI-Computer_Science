"""
Distributed Shared Memory (DSM) Library

This module implements a distributed shared memory mechanism using MPI.
It provides operations for:
- Writing values to variables (local or remote)
- Subscribing to variables
- Receiving callbacks when variables change
- Compare and exchange operations
"""

from enum import IntEnum
from typing import Dict, Set, Callable, Optional
from threading import Lock, Thread
import struct
from mpi4py import MPI

# Message types
SUBSCRIBE_MESSAGE = 1
UPDATE_MESSAGE = 2
CLOSE_MESSAGE = 3


class Message:
    """Message structure for DSM communication"""
    def __init__(self, message_type: int, rank: int, variable: int, value: int, timestamp: int = 0):
        self.message_type = message_type
        self.rank = rank
        self.variable = variable
        self.value = value
        self.timestamp = timestamp  # Lamport timestamp for total ordering
    
    def to_bytes(self) -> bytes:
        """Serialize message to bytes for MPI communication"""
        # 5 integers: message_type, rank, variable, value, timestamp
        return struct.pack('iiiii', self.message_type, self.rank, self.variable, self.value, self.timestamp)
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'Message':
        """Deserialize message from bytes"""
        message_type, rank, variable, value, timestamp = struct.unpack('iiiii', data)
        return cls(message_type, rank, variable, value, timestamp)
    
    def __lt__(self, other):
        """Compare messages for ordering: (timestamp, rank) for total ordering"""
        if self.timestamp != other.timestamp:
            return self.timestamp < other.timestamp
        return self.rank < other.rank


class DSM:
    """
    Distributed Shared Memory singleton class.
    Manages variables and subscriptions across MPI processes.
    """
    _instance = None
    _lock = Lock()
    
    def __init__(self):
        if DSM._instance is not None:
            raise RuntimeError("DSM is a singleton. Use DSM.getInstance()")
        
        self.comm = MPI.COMM_WORLD
        self.variables: Dict[int, int] = {}
        self.subscribers: Dict[int, Set[int]] = {}
        self.lock = Lock()
        self.change_callbacks: Dict[int, list] = {}  # variable -> list of callbacks
        self.lamport_clock = 0  # Lamport timestamp for total ordering
        self.pending_updates = []  # Queue for buffering updates to ensure total ordering
        self.queue_lock = Lock()
        
        # Initialize default variables
        self.variables[1] = 0
        self.variables[2] = 1
        self.variables[3] = 2
        
        # Initialize subscribers dict for each variable
        for var in self.variables:
            self.subscribers[var] = set()
            self.change_callbacks[var] = []
    
    @classmethod
    def getInstance(cls) -> 'DSM':
        """Get the singleton instance of DSM"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def get_self(self) -> int:
        """Get the rank of the current process"""
        return self.comm.Get_rank()
    
    def get_size(self) -> int:
        """Get the total number of processes"""
        return self.comm.Get_size()
    
    def setVariable(self, variable: int, value: int):
        """Set a variable value locally (thread-safe)"""
        with self.lock:
            self.variables[variable] = value
            print(f"[Rank {self.get_self()}] Variable {variable} set to {value}")
    
    def register_callback(self, variable: int, callback: Callable[[int, int, int], None]):
        """
        Register a callback function that will be called when a variable changes.
        Callback signature: callback(variable, old_value, new_value)
        """
        with self.lock:
            if variable not in self.change_callbacks:
                self.change_callbacks[variable] = []
            self.change_callbacks[variable].append(callback)
    
    def _notify_callbacks(self, variable: int, old_value: int, new_value: int):
        """Notify all registered callbacks about a variable change"""
        with self.lock:
            if variable in self.change_callbacks:
                for callback in self.change_callbacks[variable]:
                    try:
                        callback(variable, old_value, new_value)
                    except Exception as e:
                        print(f"[Rank {self.get_self()}] Error in callback: {e}")
    
    def _increment_clock(self, received_timestamp: int = 0):
        """Update Lamport clock: max(local_clock, received_timestamp) + 1"""
        with self.lock:
            self.lamport_clock = max(self.lamport_clock, received_timestamp) + 1
            return self.lamport_clock
    
    def updateVariable(self, variable: int, value: int):
        """
        Update a variable and notify all subscribers.
        This ensures all processes see changes in the same order using Lamport timestamps.
        The sender also queues its own update to ensure consistent callback ordering.
        """
        rank = self.get_self()
        
        # Check if we're subscribed to this variable
        with self.lock:
            if rank not in self.subscribers.get(variable, set()):
                print(f"[Rank {rank}] Warning: Not subscribed to variable {variable}")
                return
        
        # Increment Lamport clock for this event
        timestamp = self._increment_clock()
        
        # Create update message with timestamp
        msg = Message(UPDATE_MESSAGE, rank, variable, value, timestamp)
        
        # Send to all subscribers
        self.sendMessageToSubscribers(variable, msg)
        
        # Also queue our own update to ensure we process it in the same order as others
        # This ensures all processes (including the sender) see callbacks in the same sequence
        with self.queue_lock:
            self.pending_updates.append(msg)
        
        # Don't process immediately - let the Subscriber thread handle it
        # This ensures we wait for all messages with earlier timestamps to arrive
        # The Subscriber thread will process updates when it receives messages
    
    def checkAndReplace(self, variable: int, old_value: int, new_value: int) -> bool:
        """
        Compare and exchange operation.
        Compares variable with old_value, and if equal, sets it to new_value.
        Returns True if the exchange was performed, False otherwise.
        Only processes subscribed to the variable can perform this operation.
        """
        rank = self.get_self()
        
        # Check if we're subscribed to this variable
        with self.lock:
            if rank not in self.subscribers.get(variable, set()):
                print(f"[Rank {rank}] Warning: Not subscribed to variable {variable}, cannot perform checkAndReplace")
                return False
            
            if variable not in self.variables:
                return False
            
            if self.variables[variable] != old_value:
                return False
            
            # Value matches, proceed with update
            print(f"[Rank {rank}] Check and replace executing: {variable} {old_value} -> {new_value}")
        
        # Update variable (will notify subscribers)
        self.updateVariable(variable, new_value)
        return True
    
    def subscribeTo(self, variable: int):
        """Subscribe to a variable. All subscribers will be notified of changes."""
        rank = self.get_self()
        
        with self.lock:
            if variable not in self.subscribers:
                self.subscribers[variable] = set()
            self.subscribers[variable].add(rank)
        
        # Notify all processes about this subscription
        msg = Message(SUBSCRIBE_MESSAGE, rank, variable, -1)
        self.sendMessageToAll(msg)
    
    def syncSubscriber(self, rank: int, variable: int):
        """Synchronize subscriber information (called when receiving subscription message)"""
        with self.lock:
            if variable not in self.subscribers:
                self.subscribers[variable] = set()
            self.subscribers[variable].add(rank)
    
    def sendMessageToSubscribers(self, variable: int, msg: Message):
        """Send a message to all subscribers of a variable"""
        with self.lock:
            subs = self.subscribers.get(variable, set()).copy()
        
        for rank in subs:
            if rank != self.get_self():
                self._send_message(rank, msg)
    
    def sendMessageToAll(self, msg: Message):
        """Send a message to all processes"""
        size = self.get_size()
        for i in range(size):
            if msg.message_type == CLOSE_MESSAGE or i != self.get_self():
                self._send_message(i, msg)
    
    def _send_message(self, rank: int, msg: Message):
        """Send a message to a specific rank"""
        data = msg.to_bytes()
        self.comm.Send([data, MPI.BYTE], dest=rank, tag=0)
        print(f"[Rank {self.get_self()}] Sending message type {msg.message_type} to rank {rank} (timestamp={msg.timestamp})")
    
    def close(self):
        """Send close message to all processes"""
        msg = Message(CLOSE_MESSAGE, 0, 0, 0)
        self.sendMessageToAll(msg)
    
    def _process_pending_updates_safe(self):
        """Process pending updates in timestamp order (thread-safe, can be called from main thread)
        Only processes updates with the minimum timestamp to ensure total ordering"""
        with self.queue_lock:
            if not self.pending_updates:
                return
            
            # Sort by (timestamp, rank) for total ordering
            self.pending_updates.sort()
            
            # Find minimum timestamp
            min_timestamp = min(m.timestamp for m in self.pending_updates)
            
            # Process all updates with the minimum timestamp (in rank order)
            # This ensures we don't process later updates before earlier ones arrive
            processed = []
            for msg in self.pending_updates:
                if msg.timestamp == min_timestamp:
                    # Process the update
                    rank = self.get_self()
                    print(f"[Rank {rank}] Processing ordered update: Variable {msg.variable} = {msg.value} (timestamp={msg.timestamp}, rank={msg.rank})")
                    old_value = self.variables.get(msg.variable, 0)
                    self.setVariable(msg.variable, msg.value)
                    # Notify callbacks
                    self._notify_callbacks(msg.variable, old_value, msg.value)
                    processed.append(msg)
                else:
                    # Stop processing - we've processed all updates with min_timestamp
                    # Wait for more messages to arrive before processing higher timestamps
                    break
            
            # Remove processed messages
            for msg in processed:
                self.pending_updates.remove(msg)
    
    def printState(self):
        """Print the current state of variables and subscribers"""
        with self.lock:
            print(f"[Rank {self.get_self()}] DSM State:")
            for var, value in sorted(self.variables.items()):
                print(f"  Variable {var} = {value}")
            for var, subs in sorted(self.subscribers.items()):
                print(f"  Variable {var} subscribers: {sorted(subs)}")


class Subscriber:
    """
    Subscriber class that runs in a separate thread to receive and process messages.
    Ensures consistent ordering of variable changes across all processes using Lamport timestamps.
    """
    def __init__(self, dsm: DSM):
        self.dsm = dsm
        self.comm = dsm.comm
        self.running = False
    
    def _process_pending_updates(self):
        """Process pending updates in timestamp order to ensure total ordering"""
        # Delegate to DSM's thread-safe processing method
        self.dsm._process_pending_updates_safe()
    
    def run(self):
        """Main loop for receiving and processing messages"""
        rank = self.dsm.get_self()
        closed = False
        
        while not closed:
            print(f"[Rank {rank}] Waiting for messages...")
            
            # Receive message from any source
            # Message size is fixed: 5 integers = 20 bytes (added timestamp)
            status = MPI.Status()
            data = bytearray(20)  # Fixed-size buffer for 5 ints
            self.comm.Recv([data, MPI.BYTE], source=MPI.ANY_SOURCE, tag=0, status=status)
            
            if status.tag == 0:
                msg = Message.from_bytes(bytes(data))
                
                if msg.message_type == CLOSE_MESSAGE:
                    print(f"[Rank {rank}] Received close message. Stopping...")
                    # Process any remaining pending updates before closing
                    self._process_pending_updates()
                    closed = True
                
                elif msg.message_type == UPDATE_MESSAGE:
                    # Update Lamport clock when receiving message
                    self.dsm._increment_clock(msg.timestamp)
                    
                    print(f"[Rank {rank}] Received update message: Variable {msg.variable} updated to {msg.value} by rank {msg.rank} (timestamp={msg.timestamp})")
                    
                    # Add to pending queue for total ordering
                    with self.dsm.queue_lock:
                        self.dsm.pending_updates.append(msg)
                    
                    # Process pending updates in order (only minimum timestamp)
                    self._process_pending_updates()
                    
                    # Continue processing if there are more updates ready
                    # Keep processing until no more updates with current min_timestamp can be processed
                    while True:
                        with self.dsm.queue_lock:
                            if not self.dsm.pending_updates:
                                break
                            min_ts = min(m.timestamp for m in self.dsm.pending_updates)
                            # Check if we have any updates with min_ts that we can process
                            can_process = any(m.timestamp == min_ts for m in self.dsm.pending_updates)
                            if not can_process:
                                break
                        # Process another batch
                        self._process_pending_updates()
                
                elif msg.message_type == SUBSCRIBE_MESSAGE:
                    print(f"[Rank {rank}] Subscribe message: Rank {msg.rank} subscribes to variable {msg.variable}")
                    self.dsm.syncSubscriber(msg.rank, msg.variable)
        
        print(f"[Rank {rank}] Subscriber thread finished. Final DSM state:")
        self.dsm.printState()

