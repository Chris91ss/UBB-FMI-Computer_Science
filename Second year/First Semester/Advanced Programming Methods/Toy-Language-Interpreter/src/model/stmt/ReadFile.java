package model.stmt;

import exceptions.*;
import model.exp.Exp;
import model.state.PrgState;
import model.types.Type;
import model.values.IntValue;
import model.values.StringValue;
import model.values.Value;
import model.types.IntType;
import model.types.StringType;
import model.datastructures.MyIDictionary;

import java.io.BufferedReader;
import java.io.IOException;

public class ReadFile implements IStmt {
    private Exp exp;
    private String varName;

    public ReadFile(Exp exp, String varName) {
        this.exp = exp;
        this.varName = varName;
    }

    @Override
    public PrgState execute(PrgState state) throws StatementException {
        MyIDictionary<StringValue, BufferedReader> fileTable = state.getFileTable();
        MyIDictionary<String, Value> symTable = state.getSymTable();
        try {
            if (!symTable.isDefined(varName)) {
                throw new StatementException("Variable not declared: " + varName);
            }
            if (!symTable.lookup(varName).getType().equals(new IntType())) {
                throw new StatementException("Variable must be of type int: " + varName);
            }
            Value val = exp.eval(symTable);
            if (!val.getType().equals(new StringType())) {
                throw new StatementException("Expression must evaluate to StringType");
            }
            StringValue fileName = (StringValue) val;
            if (!fileTable.isDefined(fileName)) {
                throw new StatementException("File not opened: " + fileName.getVal());
            }
            BufferedReader br = fileTable.lookup(fileName);
            String line;
            try {
                line = br.readLine();
            } catch (IOException e) {
                throw new FileException("Error reading from file: " + e.getMessage());
            }
            int intValue;
            if (line == null) {
                intValue = 0;
            } else {
                try {
                    intValue = Integer.parseInt(line);
                } catch (NumberFormatException e) {
                    throw new StatementException("Invalid integer in file: " + line);
                }
            }
            symTable.update(varName, new IntValue(intValue));
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
        if (typeEnv.lookup(varName).equals(new IntType())) {
            return typeEnv;
        } else {
            throw new StatementException("Variable must be of type int: " + varName);
        }
    }

    @Override
    public String toString() {
        return "readFile(" + exp.toString() + ", " + varName + ")";
    }
}