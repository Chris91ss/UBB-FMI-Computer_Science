using UnityEngine;
/// Made by Mititean Cristian
public class UIDisplay : MonoBehaviour
{
    [SerializeField] private GameObject converterGameObject;
    [SerializeField] private GameObject calculatorGameObject;
    [SerializeField] private GameObject documentationGameObject;

    /// <summary>
    /// Function that swaps to the converter when the converter button was pressed
    /// </summary>
    public void SwapToConverter()
    {
        converterGameObject.SetActive(true); 
        calculatorGameObject.SetActive(false);
        documentationGameObject.SetActive(false);
    }

    /// <summary>
    /// Function that swaps to the calculator when the calculator button was pressed
    /// </summary>
    public void SwapToCalculator()
    {
        calculatorGameObject.SetActive(true);
        converterGameObject.SetActive(false);
        documentationGameObject.SetActive(false);
    }

    /// <summary>
    /// Function that swaps to the documentation when the documentation button was pressed
    /// </summary>
    public void SwapToDocumentation()
    {
        converterGameObject.SetActive(false);
        calculatorGameObject.SetActive(false);
        documentationGameObject.SetActive(true);
    }
}
