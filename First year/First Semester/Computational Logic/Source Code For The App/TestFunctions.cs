using UnityEngine;
using UnityEngine.Assertions;
/// Made by Mititean Cristian
public class TestFunctions : MonoBehaviour
{
    [SerializeField] private ConvertLogic convertLogic;
    [SerializeField] private CalculateLogic calculateLogic;

    /// <summary>
    /// call all the test functions at the start of the program
    /// </summary>
    private void Awake()
    {
        TestAllFunctions();
    }

    /// <summary>
    /// Function that calls all the test functions
    /// </summary>
    private void TestAllFunctions()
    {
        TestConvertUsingSubstitutionMethod();
        TestConvertUsingSuccessiveDivisionsMethod();
        TestConvertUsingBase10AsIntermediaryBase();
        TestRapidConversionFromBase2();
        TestRapidConversionToBase2();
        TestAddTwoNumbersInBaseP();
        TestSubtractTwoNumbersInBaseP();
        TestMultiplyNumberToDigitInBaseP();
        TestDivideNumberToDigitInBaseP();
    }

    /// <summary>
    ///  Function that tests the ConvertUsingSubstitutionMethod() function
    /// </summary>
    private void TestConvertUsingSubstitutionMethod()
    {
        Assert.AreEqual(convertLogic.ConvertUsingSubstitutionMethod("111032103", 4, 15), "1AB56");
        Assert.AreEqual(convertLogic.ConvertUsingSubstitutionMethod("5A63", 13, 5), "402011");
        Assert.AreEqual(convertLogic.ConvertUsingSubstitutionMethod("6244", 7, 15), "9AD");
    }

    /// <summary>
    /// Function that tests the ConvertUsingSuccessiveDivisionsMethod() function
    /// </summary>
    private void TestConvertUsingSuccessiveDivisionsMethod()
    {
        Assert.AreEqual(convertLogic.ConvertUsingSuccessiveDivisionsMethod("111032103", 4, 15), "1AB56");
        Assert.AreEqual(convertLogic.ConvertUsingSuccessiveDivisionsMethod("5A63", 13, 5), "402011");
        Assert.AreEqual(convertLogic.ConvertUsingSuccessiveDivisionsMethod("6244", 7, 15), "9AD");
    }

    /// <summary>
    /// Function that tests the ConvertUsingBase10AsIntermediaryBase() function
    /// </summary>
    private void TestConvertUsingBase10AsIntermediaryBase()
    {
        Assert.AreEqual(convertLogic.ConvertUsingBase10AsIntermediaryBase("111032103", 4, 15), "1AB56");
        Assert.AreEqual(convertLogic.ConvertUsingBase10AsIntermediaryBase("5A63", 13, 5), "402011");
        Assert.AreEqual(convertLogic.ConvertUsingBase10AsIntermediaryBase("6244", 7, 15), "9AD");
    }

    /// <summary>
    /// Function that tests the RapidConversionFromBase2() function
    /// </summary>
    private void TestRapidConversionFromBase2()
    {
        Assert.AreEqual(convertLogic.RapidConversionFromBase2("100010", 4), "202");
        Assert.AreEqual(convertLogic.RapidConversionFromBase2("101010", 8), "52");
        Assert.AreEqual(convertLogic.RapidConversionFromBase2("1011010", 16), "5A");
    }

    /// <summary>
    /// Function that tests the RapidConversionToBase2() function
    /// </summary>
    private void TestRapidConversionToBase2()
    {
        Assert.AreEqual(convertLogic.RapidConversionToBase2("202", 4), "100010");
        Assert.AreEqual(convertLogic.RapidConversionToBase2("52", 8), "101010");
        Assert.AreEqual(convertLogic.RapidConversionToBase2("5A", 16), "1011010");
    }

    /// <summary>
    /// Function that tests the AddTwoNumbersInBaseP() function
    /// </summary>
    private void TestAddTwoNumbersInBaseP()
    {
        Assert.AreEqual(calculateLogic.AddTwoNumbersInBaseP("123", "41", 5), "214");
        Assert.AreEqual(calculateLogic.AddTwoNumbersInBaseP("5A23", "B012C", 16), "B5B4F");
        Assert.AreEqual(calculateLogic.AddTwoNumbersInBaseP("7245", "6231", 8), "15476");
    }

    /// <summary>
    /// Function that tests the SubtractTwoNumbersInBaseP() function
    /// </summary>
    private void TestSubtractTwoNumbersInBaseP()
    {
        Assert.AreEqual(calculateLogic.SubtractTwoNumbersInBaseP("123", "41", 5), "32");
        Assert.AreEqual(calculateLogic.SubtractTwoNumbersInBaseP("5A23", "B012C", 16), "-AA709");
        Assert.AreEqual(calculateLogic.SubtractTwoNumbersInBaseP("7245", "6231", 8), "1014");
    }

    /// <summary>
    /// Function that tests the MultiplyNumberToDigitInBaseP() function
    /// </summary>
    private void TestMultiplyNumberToDigitInBaseP()
    {
        Assert.AreEqual(calculateLogic.MultiplyNumberToDigitInBaseP("123", '2', 4), "312");
        Assert.AreEqual(calculateLogic.MultiplyNumberToDigitInBaseP("128C", 'A', 16), "B978");
        Assert.AreEqual(calculateLogic.MultiplyNumberToDigitInBaseP("5173", '5', 8), "32147");
    }

    /// <summary>
    /// Function that tests the DivideNumberToDigitInBaseP() function
    /// </summary>
    private void TestDivideNumberToDigitInBaseP()
    {
        string result;
        int remainder;
        (result, remainder) = calculateLogic.DivideNumberToDigitInBaseP("123", '2', 4);
        Assert.AreEqual(result, "31");
        Assert.AreEqual(remainder, 1);
        (result, remainder) = calculateLogic.DivideNumberToDigitInBaseP("10000", '1', 2);
        Assert.AreEqual(result, "10000");
        Assert.AreEqual(remainder, 0);
        (result, remainder) = calculateLogic.DivideNumberToDigitInBaseP("67ABC56", 'A', 13);
        Assert.AreEqual(result, "877907");
        Assert.AreEqual(remainder, 1);
    }
}
