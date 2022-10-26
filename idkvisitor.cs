public class ExpressionPrintingVisitor
{
    public void PrintLiteral(Literal literal)
    {
        Console.WriteLine(literal.Value);
    }
    
    public void PrintAddition(Addition addition)
    {
        double leftValue = addition.Left.GetValue();
        double rightValue = addition.Right.GetValue();
        var sum = addition.GetValue();
        Console.WriteLine("{0} + {1} = {2}", leftValue, rightValue, sum);
    }
}

public abstract class Expression
{    
    public abstract void Accept(ExpressionPrintingVisitor v);
    
    public abstract double GetValue();
}

public class Literal : Expression
{
    public double Value { get; set; }

    public Literal(double value)
    {
        this.Value = value;
    }
    
    public override void Accept(ExpressionPrintingVisitor v)
    {
        v.PrintLiteral(this);
    }
    
    public override double GetValue()
    {
        return Value;
    }
}

public class Addition : Expression
{
    public Expression Left { get; set; }
    public Expression Right { get; set; }

    public Addition(Expression left, Expression right)
    {
        Left = left;
        Right = right;
    }
    
    public override void Accept(ExpressionPrintingVisitor v)
    {
        Left.Accept(v);
        Right.Accept(v);
        v.PrintAddition(this);
    }
    
    public override double GetValue()
    {
        return Left.GetValue() + Right.GetValue();    
    }
}

public static class Program
{
    public static void Main(string[] args)
    {
        // Emulate 1 + 2 + 3
        var e = new Addition(
            new Addition(
                new Literal(1),
                new Literal(2)
            ),
            new Literal(3)
        );
        
        var printingVisitor = new ExpressionPrintingVisitor();
        e.Accept(printingVisitor);
    }
}