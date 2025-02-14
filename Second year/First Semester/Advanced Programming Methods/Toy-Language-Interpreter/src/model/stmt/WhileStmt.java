package model.stmt;

import model.exp.Exp;
import model.state.PrgState;
import model.datastructures.*;
import model.types.Type;
import model.values.BoolValue;
import model.values.Value;
import model.types.BoolType;
import exceptions.StatementException;
import exceptions.ExpressionException;
import exceptions.ADTException;
import exceptions.DictionaryException;

public class WhileStmt implements IStmt {
    private final Exp exp;
    private final IStmt stmt;

    public WhileStmt(Exp exp, IStmt stmt) {
        this.exp = exp;
        this.stmt = stmt;
    }

    @Override
    public PrgState execute(PrgState state) throws StatementException, ExpressionException, ADTException, DictionaryException {
        MyIStack<IStmt> stack = state.getStk();
        Value condition = exp.eval(state.getSymTable());

        if (!condition.getType().equals(new BoolType())) {
            throw new StatementException("While statement error: Condition is not a boolean.");
        }

        if (((BoolValue) condition).getVal()) {
            stack.push(this); // Re-push the WhileStmt for the next iteration
            stack.push(stmt); // Push the body of the loop
        }

        return null;
    }

    @Override
    public MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException, ExpressionException, DictionaryException {
        Type expType = exp.typecheck(typeEnv);
        if (!expType.equals(new BoolType())) {
            throw new StatementException("While statement error: Condition is not a boolean.");
        }

        stmt.typecheck(typeEnv);
        return typeEnv;
    }

    @Override
    public String toString() {
        return "while(" + exp.toString() + ") " + stmt.toString();
    }
}
