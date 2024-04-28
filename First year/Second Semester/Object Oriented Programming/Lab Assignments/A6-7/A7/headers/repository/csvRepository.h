#include "repository.h"
#include <fstream>
#include "utilities/exceptions.h"

class CSVRepository : public Repository
{
private:
    string fileName;
public:
    explicit CSVRepository(string fileName);
    void WriteToFile() override;
    void OpenInApplication() override;
};