package model.stmt;

import exceptions.*;
import model.exp.Exp;
import model.state.PrgState;
import model.values.StringValue;
import model.values.Value;
import model.types.StringType;
import model.datastructures.MyIDictionary;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class OpenRFile implements IStmt {
    private Exp exp;

    public OpenRFile(Exp exp) {
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
            if (fileTable.isDefined(fileName)) {
                throw new StatementException("File already opened: " + fileName.getVal());
            }
            BufferedReader br;
            try {
                br = new BufferedReader(new FileReader(fileName.getVal()));
            } catch (IOException e) {
                throw new FileException("Error opening file: " + e.getMessage());
            }
            fileTable.add(fileName, br);
        } catch (ExpressionException | ADTException | FileException e) {
            throw new StatementException(e.getMessage());
        }
        return null;
    }

    @Override
    public String toString() {
        return "openRFile(" + exp.toString() + ")";
    }
}