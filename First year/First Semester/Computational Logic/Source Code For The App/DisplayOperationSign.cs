using UnityEngine;
/// Made by Mititean Cristian
public class DisplayOperationSign : MonoBehaviour
{
    [SerializeField] private TMPro.TMP_Dropdown operationMethodDropdown;
    [SerializeField] private GameObject plusSignText;
    [SerializeField] private GameObject minusSignText;
    [SerializeField] private GameObject multiplicationSignText;
    [SerializeField] private GameObject divisionSignText;

    private void Update()
    {
        /// We display the operation based on what the user has selected from the operation dropdown
        if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Add 2 numbers in base p")
        {
            plusSignText.SetActive(true);
            minusSignText.SetActive(false);
            multiplicationSignText.SetActive(false);
            divisionSignText.SetActive(false);
        }
        else if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Subtract 2 numbers in base p")
        {
            plusSignText.SetActive(false);
            minusSignText.SetActive(true);
            multiplicationSignText.SetActive(false);
            divisionSignText.SetActive(false);
        }
        else if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Multiply a number to a digit in base p")
        {
            plusSignText.SetActive(false);
            minusSignText.SetActive(false);
            multiplicationSignText.SetActive(true);
            divisionSignText.SetActive(false);
        }
        else if (operationMethodDropdown.options[operationMethodDropdown.value].text == "Divide a number to a digit in base p")
        {
            plusSignText.SetActive(false);
            minusSignText.SetActive(false);
            multiplicationSignText.SetActive(false);
            divisionSignText.SetActive(true);
        }
    }
}
