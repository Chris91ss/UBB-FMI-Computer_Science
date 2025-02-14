package exceptions;

public class ProgramStateException extends InterpreterException {
    public ProgramStateException(String message) {
        super(message);
    }
}