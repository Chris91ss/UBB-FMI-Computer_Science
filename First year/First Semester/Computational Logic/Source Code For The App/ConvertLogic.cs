using System;
using System.Collections.Generic;
using UnityEngine;
/// Made by Mititean Cristian
public class ConvertLogic : MonoBehaviour
{
    [SerializeField] private CalculateLogic calculateLogic;

    [SerializeField] private TMPro.TMP_Dropdown operationMethodDropdown;
    [SerializeField] private TMPro.TMP_Dropdown fromBaseDropdown;
    [SerializeField] private TMPro.TMP_Dropdown toBaseDropdown;
    [SerializeField] private TMPro.TMP_Text resultText;

    private string numberInput;
    private int fromBaseValue;
    private int toBaseValue;
    private string resultValue;

    private void Update()
    {
        GetFromBaseValue();
        GetToBaseValue();
    }

    /// <summary>
    /// Gets the base from the option string in the fromBaseDropdown and converts it to int
    /// </summary>
    private void GetFromBaseValue()
    {
        string[] splitStringFromBase = fromBaseDropdown.options[fromBaseDropdown.value].text.Split(" ");
        int.TryParse(splitStringFromBase[1], out fromBaseValue);
        //Debug.Log(fromBaseValue);
    }

    /// <summary>
    /// Gets the base from the option string in the toBaseDropdown and converts it to int
    /// </summary>
    private void GetToBaseValue()
    {
        string[] splitStringToBase = toBaseDropdown.options[toBaseDropdown.value].text.Split(" ");
        int.TryParse(splitStringToBase[1], out toBaseValue);
        //Debug.Log(toBaseValue);
    }

    /// <summary>
    /// Reads the input from the input field in the UI and stores it in numberInput
    /// </summary>
    public void ReadInputValue(string inputValue)
    {
        numberInput = inputValue;
        Debug.Log(numberInput);
    }

    /// <summary>
    /// Function that gets called whenever we press the convert button
    /// </summary>
    public void ConvertButton()
    {
        CheckOperationMethodAndCovert();
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
    private void CheckOperationMethodAndCovert()
    {
        try
        {
            SetResultColor(Color.green);
            if (!CheckIfNumberIsAvailableInBaseB(numberInput, fromBaseValue))
            {
                SetResultColor(Color.red);
                resultValue = "Input values are not valid!";
            }
            else
            {
                if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Convert using base 10 as an intermediary base")
                {
                    resultValue = ConvertUsingBase10AsIntermediaryBase(numberInput, fromBaseValue, toBaseValue);
                }
                else if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Convert using rapid conversions")
                {
                    if (CheckIfRapidConversionIsAvailable(fromBaseValue, toBaseValue))
                    {
                        if (fromBaseValue == 2)
                            resultValue = RapidConversionFromBase2(numberInput, toBaseValue);
                        else
                            resultValue = RapidConversionToBase2(numberInput, fromBaseValue);
                    }
                    else
                    {
                        SetResultColor(Color.red);
                        resultValue = "Input values are not valid!";
                    }
                }
                else if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Convert using substitution method")
                {
                    resultValue = ConvertUsingSubstitutionMethod(numberInput, fromBaseValue, toBaseValue);
                }
                else if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Convert using successive divisions method")
                {
                    resultValue = ConvertUsingSuccessiveDivisionsMethod(numberInput, fromBaseValue, toBaseValue);
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
    /// Function that checks if rapid conversion is available
    /// </summary>
    /// <param name="fromBase">source base</param>
    /// <param name="toBase">destination base</param>
    /// <returns>True if rapid conversion is available, false otherwise</returns>
    private bool CheckIfRapidConversionIsAvailable(int fromBase, int toBase)
    {
        if (fromBase == 2 && (toBase == 4 || toBase == 8 || toBase == 16))
            return true;

        if (toBase == 2 && (fromBase == 4 || fromBase == 8 || fromBase == 16))
            return true;

        return false;
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
    /// Function that converts the given number in a source base to the number in the destination base using the Substitution Method
    /// </summary>
    /// <param name="number">number given by the user</param>
    /// <param name="fromBase">source base selected by the user</param>
    /// <param name="toBase">destination base selected by the user</param>
    /// <returns>The number in the destination base</returns>
    public string ConvertUsingSubstitutionMethod(string number, int fromBase, int toBase)
    {
        List<char> listOfDigits = new List<char> { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G' };

        char fromBaseDigit = listOfDigits[fromBase];
        int index = number.Length - 1;
        string res = "";
        string mult = "1";

        while (index >= 0)
        {
            char dig = number[index];
            string currentNumber = calculateLogic.MultiplyNumberToDigitInBaseP(mult, dig, toBase);
            res = calculateLogic.AddTwoNumbersInBaseP(res, currentNumber, toBase);
            mult = calculateLogic.MultiplyNumberToDigitInBaseP(mult, fromBaseDigit, toBase);
            index--;
        }

        while (res.Length > 0 && res[0] == '0')
        {
            res = res[1..];
        }

        return res;
    }

    /// <summary>
    /// Function that converts the given number in a source base to the number in the destination base using the Successive Divisions Method
    /// </summary>
    /// <param name="number">number given by the user</param>
    /// <param name="fromBase">source base selected by the user</param>
    /// <param name="toBase">destination base selected by the user</param>
    /// <returns>The number in the destination base</returns>
    public string ConvertUsingSuccessiveDivisionsMethod(string number, int fromBase, int toBase)
    {
        List<char> listOfDigits = new List<char> { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' };

        char toBaseDigit = listOfDigits[toBase];
        string res = "";

        while (number != "0")
        {
            (string newA, int remainder) = calculateLogic.DivideNumberToDigitInBaseP(number, toBaseDigit, fromBase);

            char currentDigitOfNumber = listOfDigits[remainder];
            number = newA;

            res = currentDigitOfNumber + res;
        }

        // Ensure that the result is not an empty string
        if (res.Length == 0)
        {
            res = "0";
        }

        return res;
    }

    /// <summary>
    /// Function that converts the given number in a source base to the number in the destination base using Base_10 as an Intermediary Base
    /// </summary>
    /// <param name="number">number given by the user</param>
    /// <param name="fromBase">source base selected by the user</param>
    /// <param name="toBase">destination base selected by the user</param>
    /// <returns>The number in the destination base</returns>
    public string ConvertUsingBase10AsIntermediaryBase(string number, int fromBase, int toBase)
    {
        string resultInBase10;

        resultInBase10 = ConvertUsingSubstitutionMethod(number, fromBase, 10);
        return ConvertUsingSuccessiveDivisionsMethod(resultInBase10, 10, toBase);
    }

    /// <summary>
    /// Function that converts the given number from Base_2 to the number in the destination base using Rapid Conversion 
    /// </summary>
    /// <param name="number">number given by the user</param>
    /// <param name="numBase">destination base selected by the user</param>
    /// <returns>The number in the destination base (Important Note -> destination base must be a power of 2)</returns>
    public string RapidConversionFromBase2(string number, int numBase)
    {
        Dictionary<int, string[]> correspondenceTable = new Dictionary<int, string[]>
        {
            {2, new string[] {"0", "1", "10", "11", "100", "101", "110", "111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"}},
            {4, new string[] {"0", "1", "2", "3", "10", "11", "12", "13", "20", "21", "22", "23", "30", "31", "32", "33"}},
            {8, new string[] {"0", "1", "2", "3", "4", "5", "6", "7", "10", "11", "12", "13", "14", "15", "16", "17"}},
            {16, new string[] {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"}},
        };

        int numberIndex = number.Length - 1;
        int amountOfDigitsWeTake = (int)Math.Log(numBase, 2);
        string result = "";

        while (numberIndex >= 0)
        {
            string group = "";

            for (int i = 0; i < amountOfDigitsWeTake; i++)
            {
                if (numberIndex >= 0)
                {
                    group = number[numberIndex] + group;
                    numberIndex--;
                }
            }

            while (group[0] == '0' && group.Length > 1)
            {
                group = group.Substring(1);
            }

            result = correspondenceTable[numBase][Array.IndexOf(correspondenceTable[2], group)] + result;
        }

        return result;
    }

    /// <summary>
    /// Function that converts the given number from the source base to the number in Base_2 using Rapid Conversion 
    /// </summary>
    /// <param name="number">number given by the user</param>
    /// <param name="numBase">source base selected by the user</param>
    /// <returns>The number in Base_2 (Important Note -> source base must be a power of 2)</returns>
    public string RapidConversionToBase2(string number, int numBase)
    {
        Dictionary<int, string[]> correspondenceTable = new Dictionary<int, string[]>
        {
            {2, new string[] {"0", "1", "10", "11", "100", "101", "110", "111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"}},
            {4, new string[] {"0", "1", "2", "3", "10", "11", "12", "13", "20", "21", "22", "23", "30", "31", "32", "33"}},
            {8, new string[] {"0", "1", "2", "3", "4", "5", "6", "7", "10", "11", "12", "13", "14", "15", "16", "17"}},
            {16, new string[] {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"}},
        };

        int amountOfDigitsWeTake = (int)Math.Log(numBase, 2);
        int numberIndex = number.Length - 1;
        string result = "";

        while (numberIndex >= 0)
        {
            string group = correspondenceTable[2][Array.IndexOf(correspondenceTable[numBase], number[numberIndex].ToString())];
            numberIndex--;

            while (group.Length < amountOfDigitsWeTake)
            {
                group = "0" + group;
            }

            result = group + result;
        }

        while (result.Length > 1 && result[0] == '0')
        {
            result = result.Substring(1);
        }

        return result;
    }
}
