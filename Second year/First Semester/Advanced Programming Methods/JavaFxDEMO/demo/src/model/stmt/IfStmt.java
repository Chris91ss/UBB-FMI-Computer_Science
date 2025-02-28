package model.stmt;

import exceptions.ADTException;
import model.datastructures.MyIDictionary;
import model.state.PrgState;
import model.exp.Exp;
import model.datastructures.MyIStack;
import model.types.Type;
import model.values.Value;
import model.values.BoolValue;
import model.types.BoolType;
import exceptions.StatementException;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public class IfStmt implements IStmt {
    private Exp exp;
    private IStmt thenS;
    private IStmt elseS;

    public IfStmt(Exp exp, IStmt thenS, IStmt elseS) {
        this.exp = exp;
        this.thenS = thenS;
        this.elseS = elseS;
    }

    @Override
    public PrgState execute(PrgState state) throws StatementException {
        try {
            Value cond = exp.eval(state.getSymTable());
            if (!cond.getType().equals(new BoolType())) {
                throw new StatementException("Conditional expression is not a boolean");
            }
            BoolValue boolCond = (BoolValue) cond;
            MyIStack<IStmt> stack = state.getStk();
            if (boolCond.getVal()) {
                stack.push(thenS);
            } else {
                stack.push(elseS);
            }
        } catch (ExpressionException | ADTException e) {
            throw new StatementException(e.getMessage());
        }
        return null;
    }

    @Override
    public MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException, ExpressionException, DictionaryException {
        Type expType = exp.typecheck(typeEnv);
        if (!expType.equals(new BoolType())) {
            throw new StatementException("Conditional expression must be of type BoolType");
        }
        thenS.typecheck(typeEnv);
        elseS.typecheck(typeEnv);
        return typeEnv;
    }

    @Override
    public String toString() {
        return "If(" + exp.toString() + ") Then(" + thenS.toString() + ") Else(" + elseS.toString() + ")";
    }
}
