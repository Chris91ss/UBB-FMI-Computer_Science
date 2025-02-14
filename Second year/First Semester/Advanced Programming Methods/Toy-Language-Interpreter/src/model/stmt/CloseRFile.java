package model.stmt;

import exceptions.*;
import model.exp.Exp;
import model.state.PrgState;
import model.types.Type;
import model.values.StringValue;
import model.values.Value;
import model.types.StringType;
import model.datastructures.MyIDictionary;

import java.io.BufferedReader;
import java.io.IOException;

public class CloseRFile implements IStmt {
    private Exp exp;

    public CloseRFile(Exp exp) {
        this.exp = exp;
    }

    @Override
    public PrgState execute(PrgState state) throws StatementException {
        MyIDictionary<StringValue, BufferedReader> fileTable = state.getFileTable();
        try {
            Value val = exp.eval(state.getSymTable());
            if (!val.getType().equals(new StringType())) {
                throw new StatementException("Expression must evaluate to StringType");
            }
            StringValue fileName = (StringValue) val;
            if (!fileTable.isDefined(fileName)) {
                throw new StatementException("File not opened: " + fileName.getVal());
            }
            BufferedReader br = fileTable.lookup(fileName);
            try {
                br.close();
            } catch (IOException e) {
                throw new FileException("Error closing file: " + e.getMessage());
            }
            fileTable.remove(fileName);
        } catch (ExpressionException | ADTException | FileException e) {
            throw new StatementException(e.getMessage());
        }
        return null;
    }

    @Override
    public MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException, ExpressionException, DictionaryException {
        Type expType = exp.typecheck(typeEnv);
        if (!expType.equals(new StringType())) {
            throw new StatementException("Expression must evaluate to StringType");
        }
        return typeEnv;
    }

    @Override
    public String toString() {
        return "closeRFile(" + exp.toString() + ")";
    }
}