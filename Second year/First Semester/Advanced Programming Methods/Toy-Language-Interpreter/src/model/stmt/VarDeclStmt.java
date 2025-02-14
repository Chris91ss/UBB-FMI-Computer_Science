package model.stmt;

import exceptions.ExpressionException;
import model.state.PrgState;
import model.datastructures.MyIDictionary;
import model.values.Value;
import model.types.Type;
import exceptions.StatementException;
import exceptions.DictionaryException;

public class VarDeclStmt implements IStmt {
    private String id;
    private Type type;

    public VarDeclStmt(String id, Type type) {
        this.id = id;
        this.type = type;
    }

    @Override
    public PrgState execute(PrgState state) throws StatementException {
        MyIDictionary<String, Value> symTbl = state.getSymTable();
        if (symTbl.isDefined(id)) {
            throw new StatementException("Variable '" + id + "' already declared");
        } else {
            try {
                symTbl.add(id, type.defaultValue());
            } catch (DictionaryException e) {
                throw new StatementException(e.getMessage());
            }
        }
        return null;
    }

    @Override
    public MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException, ExpressionException, DictionaryException {
        typeEnv.add(id, type);
        return typeEnv;
    }

    @Override
    public String toString() {
        return type.toString() + " " + id;
    }
}
