#include "repository.h"
#include <fstream>
#include "../../headers/utilities/exceptions.h"

class CSVRepository : public Repository
{
private:
    string fileName;
public:
    explicit CSVRepository(string fileName);
    void Add(const TrenchCoat& trenchCoat) override;
    void RemoveByValue(const TrenchCoat& trenchCoat) override;
    void WriteToFile() override;
    void ReadFromFile() override;
    void OpenInApplication() override;
};