package model.values;

import model.types.StringType;
import model.types.Type;

public class StringValue implements Value {
    private String val;

    public StringValue(String val) {
        this.val = val;
    }

    public String getVal() {
        return val;
    }

    @Override
    public Type getType() {
        return new StringType();
    }

    @Override
    public boolean equals(Object another) {
        if (another instanceof StringValue) {
            return val.equals(((StringValue) another).getVal());
        }
        return false;
    }

    @Override
    public String toString() {
        return "\"" + val + "\"";
    }
}