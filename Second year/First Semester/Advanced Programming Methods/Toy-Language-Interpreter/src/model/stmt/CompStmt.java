package model.stmt;

import exceptions.DictionaryException;
import exceptions.ExpressionException;
import model.datastructures.MyIDictionary;
import model.state.PrgState;
import model.datastructures.MyIStack;
import exceptions.StatementException;
import model.types.Type;

public class CompStmt implements IStmt {
    private IStmt first;
    private IStmt second;

    public CompStmt(IStmt first, IStmt second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public PrgState execute(PrgState state) throws StatementException {
        MyIStack<IStmt> stack = state.getStk();
        stack.push(second);
        stack.push(first);
        return null;
    }

    @Override
    public MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException, ExpressionException, DictionaryException {
        return second.typecheck(first.typecheck(typeEnv));
    }

    @Override
    public String toString() {
        return "(" + first.toString() + "; " + second.toString() + ")";
    }
}
