using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UIElements;
/// Made by Mititean Cristian
public class CalculateLogic : MonoBehaviour
{
    [SerializeField] private TMPro.TMP_Dropdown operationMethodDropdown;
    [SerializeField] private TMPro.TMP_Dropdown baseDropdown;
    [SerializeField] private TMPro.TMP_Text resultText;

    private string firstNumberInput;
    private string secondNumberInput;
    private int baseValue;
    private string resultValue;

    private void Update()
    {
        GetBaseValue();
    }

    /// <summary>
    /// Gets the base from the option string in the baseDropdown and converts it to int
    /// </summary>
    private void GetBaseValue()
    {
        string[] splitStringBase = baseDropdown.options[baseDropdown.value].text.Split(" ");
        int.TryParse(splitStringBase[1], out baseValue);
        //Debug.Log(baseValue);
    }

    /// <summary>
    /// Reads the input from the first number input field in the UI and stores it in firstNumberInput
    /// </summary>
    public void ReadFirstNumberInput(string inputValue)
    {
        firstNumberInput = inputValue;
        Debug.Log(firstNumberInput);
    }

    /// <summary>
    /// Reads the input from the second number input field in the UI and stores it in secondNumberInput
    /// </summary>
    public void ReadSecondNumberInput(string inputValue)
    {
        secondNumberInput = inputValue;
        Debug.Log(secondNumberInput);
    }

    /// <summary>
    /// Function that gets called whenever we press the calculate button
    /// </summary>
    public void CalculateButton()
    {
        CheckOperationMethodAndCalculate();
    }

    /// <summary>
    /// sets the result text in the UI
    /// </summary>
    public void SetResultText()
    {
        resultText.text = resultValue;
    }

    /// <summary>
    /// Function that changes the color of the result text
    /// </summary>
    /// <param name="color">color of the text</param>
    private void SetResultColor(Color color)
    {
        resultText.color = color;
    }

    /// <summary>
    /// Function that deals with checking the user input and calling the proper function based on that input
    /// </summary>
    private void CheckOperationMethodAndCalculate()
    {
        try
        {
            SetResultColor(Color.green);
            if (!CheckIfNumberIsAvailableInBaseB(firstNumberInput, baseValue) || !CheckIfNumberIsAvailableInBaseB(secondNumberInput, baseValue))
            {

                SetResultColor(Color.red);
                resultValue = "Input values are not valid!";
            }
            else
            {
                if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Add 2 numbers in base p")
                {
                    resultValue = AddTwoNumbersInBaseP(firstNumberInput, secondNumberInput, baseValue);
                }
                else if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Subtract 2 numbers in base p")
                {
                    resultValue = SubtractTwoNumbersInBaseP(firstNumberInput, secondNumberInput, baseValue);
                }
                else if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Multiply a number to a digit in base p")
                {
                    if (secondNumberInput.Length == 1)
                        resultValue = MultiplyNumberToDigitInBaseP(firstNumberInput, secondNumberInput[0], baseValue);
                    else
                    {

                        SetResultColor(Color.red);
                        resultValue = "Input values are not valid!";
                    }
                }
                else if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Divide a number to a digit in base p")
                {
                    if (secondNumberInput.Length == 1)
                    {
                        int remainder;
                        (resultValue, remainder) = DivideNumberToDigitInBaseP(firstNumberInput, secondNumberInput[0], baseValue);
                        resultValue = resultValue + " remainder: " + remainder.ToString();
                    }
                    else
                    {
                        SetResultColor(Color.red);
                        resultValue = "Input values are not valid!";
                    }
                }
            }
        }
        catch (Exception ex)
        {
            Debug.Log($"Exception caught: {ex.Message}");
            SetResultColor(Color.red);
            resultValue = "No valid inputs were read.";
        }
    }

    /// <summary>
    /// Function that checks if the number is valid in the given base
    /// </summary>
    /// <param name="number">number given by the user</param>
    /// <param name="numBase">source base selected by the user</param>
    /// <returns>True if the number in the given base is valid, false otherwise</returns>
    private static bool CheckIfNumberIsAvailableInBaseB(string number, int numBase)
    {
        List<char> listOfDigits = new List<char> { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' };

        foreach (char digit in number)
        {
            if (!listOfDigits.Contains(digit))
            {
                return false;
            }

            int digitIndex = listOfDigits.IndexOf(digit);

            if (digitIndex >= numBase)
            {
                return false;
            }
        }

        return true;
    }

    /// <summary>
    /// Function that add two numbers in base p
    /// </summary>
    /// <param name="firstNumber">first number given by the user</param>
    /// <param name="secondNumber">second number given by the user</param>
    /// <param name="p">base selected by the user</param>
    /// <returns>The result of addition</returns>
    public string AddTwoNumbersInBaseP(string firstNumber, string secondNumber, int p)
    {
        List<char> listOfDigits = new List<char> { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' };
        int firstNumberIndex = firstNumber.Length - 1;
        int secondNumberIndex = secondNumber.Length - 1;

        int remainder = 0;
        string result = "";

        while (firstNumberIndex >= 0 || secondNumberIndex >= 0)
        {
            int digitOfFirstNumber = 0;
            if (firstNumberIndex >= 0)
            {
                digitOfFirstNumber = listOfDigits.IndexOf(firstNumber[firstNumberIndex]);
                firstNumberIndex--;
            }

            int digitOfSecondNumber = 0;
            if (secondNumberIndex >= 0)
            {
                digitOfSecondNumber = listOfDigits.IndexOf(secondNumber[secondNumberIndex]);
                secondNumberIndex--;
            }

            char currentDigitOfNumber = listOfDigits[(digitOfFirstNumber + digitOfSecondNumber + remainder) % p];
            remainder = (digitOfFirstNumber + digitOfSecondNumber + remainder) / p;

            result = currentDigitOfNumber + result;
        }

        if (remainder > 0)
        {
            char currentDigitOfNumber = listOfDigits[remainder];
            result = currentDigitOfNumber + result;
        }

        return result;
    }

    /// <summary>
    /// Function that checks if the first number is greater than the second one, if not, we swap them and mark it with a '-' so we know that we swapped them
    /// </summary>
    /// <param name="firstNumber">first number given by the user</param>
    /// <param name="secondNumber">second number given by the user</param>
    private (string, string, string) GreaterNumbers(string firstNumber, string secondNumber)
    {
        if (firstNumber.Length > secondNumber.Length)
            return (firstNumber, secondNumber, "");
        if (firstNumber.Length < secondNumber.Length)
            return (secondNumber, firstNumber, "-");
        for (int i = 0; i < firstNumber.Length; i++)
        {
            if (firstNumber[i] > secondNumber[i])
                return (firstNumber, secondNumber, "");
            if (firstNumber[i] < secondNumber[i])
                return (secondNumber, firstNumber, "-");
        }
        return (firstNumber, secondNumber, "");
    }

    /// <summary>
    /// Function that substracts two numbers in base p
    /// </summary>
    /// <param name="firstNumber">first number given by the user</param>
    /// <param name="secondNumber">second number given by the user</param>
    /// <param name="p">base selected by the user</param>
    /// <returns>The result of substraction</returns>
    public string SubtractTwoNumbersInBaseP(string firstNumber, string secondNumber, int p)
    {
        List<char> listOfDigits = new List<char> { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' };

        (string, string, string) resultTuple = GreaterNumbers(firstNumber, secondNumber);
        string greaterNumber = resultTuple.Item1;
        string smallerNumber = resultTuple.Item2;
        string sign = resultTuple.Item3;

        int firstNumberIndex = greaterNumber.Length - 1;
        int secondNumberIndex = smallerNumber.Length - 1;
        int borrow = 0;
        string result = "";

        while (firstNumberIndex >= 0 || borrow > 0)
        {
            int digitOfFirstNumber = 0;
            if (firstNumberIndex >= 0)
            {
                digitOfFirstNumber = listOfDigits.IndexOf(greaterNumber[firstNumberIndex]) - borrow;
                firstNumberIndex--;
            }
            else
            {
                digitOfFirstNumber = 0 - borrow;
            }

            int digitOfSecondNumber = 0;
            if (secondNumberIndex >= 0)
            {
                digitOfSecondNumber = listOfDigits.IndexOf(smallerNumber[secondNumberIndex]);
                secondNumberIndex--;
            }

            if (digitOfFirstNumber < digitOfSecondNumber)
            {
                digitOfFirstNumber += p;
                borrow = 1;
            }
            else
            {
                borrow = 0;
            }

            char currentDigitOfNumber = listOfDigits[digitOfFirstNumber - digitOfSecondNumber];
            result = currentDigitOfNumber + result;
        }

        while (result[0] == '0' && result.Length > 1)
        {
            result = result[1..];
        }

        result = sign + result;
        return result;
    }

    /// <summary>
    /// Function that multiplies a number with a digit in base p
    /// </summary>
    /// <param name="firstNumber">first number given by the user</param>
    /// <param name="secondNumber">second number given by the user</param>
    /// <param name="p">base selected by the user</param>
    /// <returns>The result of multiplication</returns>
    public string MultiplyNumberToDigitInBaseP(string firstNumber, char secondNumber, int p)
    {
        List<char> listOfDigits = new List<char> { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' , 'G'};

        int firstNumberIndex = firstNumber.Length - 1;
        int digitOfSecondNumber = listOfDigits.IndexOf(secondNumber);

        string result = "";
        int carry = 0;

        while (firstNumberIndex >= 0 || carry > 0)
        {
            int digitOfFirstNumber = 0;
            if (firstNumberIndex >= 0)
            {
                digitOfFirstNumber = listOfDigits.IndexOf(firstNumber[firstNumberIndex]);
                firstNumberIndex--;
            }

            int product = (digitOfFirstNumber * digitOfSecondNumber) + carry;
            int currentDigitOfNumber = product % p;
            carry = product / p;

            result = listOfDigits[currentDigitOfNumber] + result;
        }

        return result;
    }

    /// <summary>
    /// Function that divides a number with a digit in base p
    /// </summary>
    /// <param name="firstNumber">first number given by the user</param>
    /// <param name="secondNumber">second number given by the user</param>
    /// <param name="p">base selected by the user</param>
    /// <returns>The result of division with remainder</returns>
    public (string, int) DivideNumberToDigitInBaseP(string firstNumber, char secondNumber, int p)
    {
        List<char> listOfDigits = new List<char> { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' };

        int digitOfSecondNumber = listOfDigits.IndexOf(secondNumber);

        string result = "";
        int remainder = 0;

        foreach (char digitOfFirstNumber in firstNumber)
        {
            int digitOfNrValue = listOfDigits.IndexOf(digitOfFirstNumber);

            char currentDigitOfNumber = listOfDigits[(remainder * p + digitOfNrValue) / digitOfSecondNumber];
            remainder = (remainder * p + digitOfNrValue) % digitOfSecondNumber;

            result += currentDigitOfNumber;
        }

        while (result[0] == '0' && result.Length > 1)
        {
            result = result[1..];
        }

        return (result, remainder);
    }
}
