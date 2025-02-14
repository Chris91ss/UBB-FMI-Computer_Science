package model.stmt;

import exceptions.DictionaryException;
import exceptions.ExpressionException;
import model.datastructures.MyIDictionary;
import model.state.PrgState;
import exceptions.StatementException;
import exceptions.InterpreterException;
import model.types.Type;

public interface IStmt {
    PrgState execute(PrgState state) throws StatementException, InterpreterException;
    MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException, ExpressionException, DictionaryException;
}
