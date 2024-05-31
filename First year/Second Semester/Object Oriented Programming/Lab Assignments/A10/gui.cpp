#include "gui.h"
#include "ui_GUI.h"


GUI::GUI(QWidget *parent, const Service &service) : QWidget(parent), ui(new Ui::GUI), service(service){
    ui->setupUi(this);

    this->adminWindow = new QWidget();
    this->userWindow = new QWidget();
    this->entryWindow = new QWidget();

    // ------------------ entry window ------------------

    // entry layout
    this->entryLayout = new QGridLayout();
    this->adminButton = new QPushButton("Admin");
    this->userCSVButton = new QPushButton("User CSV");
    this->userHTMLButton = new QPushButton("User HTML");
    this->entryLayout->addWidget(this->adminButton, 0, 0);
    this->entryLayout->addWidget(this->userCSVButton, 1, 0);
    this->entryLayout->addWidget(this->userHTMLButton, 2, 0);

    // add the layout to the admin window
    this->entryWindow->setLayout(this->entryLayout);

    // style the admin form
    this->entryWindow->setWindowTitle("Entry Window");
    this->entryWindow->setFixedSize(450, 475);

    // ------------------ admin window ------------------

    // admin layout
    this->adminLayout = new QHBoxLayout();
    this->adminOutputLayout = new QVBoxLayout();
    this->adminCommandsLayout = new QVBoxLayout();
    this->adminAddLayout = new QGridLayout();
    this->adminRemoveLayout = new QGridLayout();
    this->adminUpdateLayout = new QGridLayout();
    this->adminUndoRedoLayout = new QGridLayout();

    // admin output elements
    this->adminList = new QListWidget();
    this->adminOutputLine = new QLineEdit();
    this->adminOutputLine->setReadOnly(true);

    // admin buttons
    this->adminAddButton = new QPushButton("Add");
    this->adminRemoveButton = new QPushButton("Remove");
    this->adminUpdateButton = new QPushButton("Update");
    this->adminBackButton = new QPushButton("Back");
    this->adminUndoButton = new QPushButton("Undo");
    this->adminRedoButton = new QPushButton("Redo");

    // admin add input fields
    this->adminAddSizeLine = new QLineEdit();
    this->adminAddColorLine = new QLineEdit();
    this->adminAddPriceLine = new QLineEdit();
    this->adminAddQuantityLine = new QLineEdit();
    this->adminAddPhotoLine = new QLineEdit();
    // admin add labels
    this->adminAddSizeLabel = new QLabel("Size");
    this->adminAddColorLabel = new QLabel("Color");
    this->adminAddPriceLabel = new QLabel("Price");
    this->adminAddQuantityLabel = new QLabel("Quantity");
    this->adminAddPhotoLabel = new QLabel("Photo");

    // admin remove input fields
    this->adminRemoveSizeLine = new QLineEdit();
    this->adminRemoveColorLine = new QLineEdit();
    // admin remove labels
    this->adminRemoveSizeLabel = new QLabel("Size");
    this->adminRemoveColorLabel = new QLabel("Color");

    // admin update input fields
    this->adminUpdateSizeLine = new QLineEdit();
    this->adminUpdateColorLine = new QLineEdit();
    this->adminUpdatePriceLine = new QLineEdit();
    this->adminUpdateQuantityLine = new QLineEdit();
    this->adminUpdatePhotoLine = new QLineEdit();
    // admin update labels
    this->adminUpdateSizeLabel = new QLabel("Size");
    this->adminUpdateColorLabel = new QLabel("Color");
    this->adminUpdatePriceLabel = new QLabel("Price");
    this->adminUpdateQuantityLabel = new QLabel("Quantity");
    this->adminUpdatePhotoLabel = new QLabel("Photo");

    // add layouts to the form
    this->adminLayout->addLayout(this->adminOutputLayout);
    this->adminLayout->addLayout(this->adminCommandsLayout);
    this->adminCommandsLayout->addLayout(this->adminAddLayout);
    this->adminCommandsLayout->addLayout(this->adminRemoveLayout);
    this->adminCommandsLayout->addLayout(this->adminUpdateLayout);
    this->adminCommandsLayout->addLayout(this->adminUndoRedoLayout);
    this->adminCommandsLayout->addWidget(this->adminBackButton);

    // add the elements to the output layout
    this->adminOutputLayout->addWidget(this->adminList);
    this->adminOutputLayout->addWidget(this->adminOutputLine);

    // add the elements to the add layout
    this->adminAddLayout->addWidget(this->adminAddSizeLabel, 0, 0);
    this->adminAddLayout->addWidget(this->adminAddSizeLine, 0, 1);
    this->adminAddLayout->addWidget(this->adminAddColorLabel, 1, 0);
    this->adminAddLayout->addWidget(this->adminAddColorLine, 1, 1);
    this->adminAddLayout->addWidget(this->adminAddPriceLabel, 2, 0);
    this->adminAddLayout->addWidget(this->adminAddPriceLine, 2, 1);
    this->adminAddLayout->addWidget(this->adminAddQuantityLabel, 3, 0);
    this->adminAddLayout->addWidget(this->adminAddQuantityLine, 3, 1);
    this->adminAddLayout->addWidget(this->adminAddPhotoLabel, 4, 0);
    this->adminAddLayout->addWidget(this->adminAddPhotoLine, 4, 1);
    this->adminAddLayout->addWidget(this->adminAddButton, 5, 0, 1, 2);

    // add the elements to the remove layout
    this->adminRemoveLayout->addWidget(this->adminRemoveSizeLabel, 0, 0);
    this->adminRemoveLayout->addWidget(this->adminRemoveSizeLine, 0, 1);
    this->adminRemoveLayout->addWidget(this->adminRemoveColorLabel, 1, 0);
    this->adminRemoveLayout->addWidget(this->adminRemoveColorLine, 1, 1);
    this->adminRemoveLayout->addWidget(this->adminRemoveButton, 2, 0, 1, 2);

    // add the elements to the update layout
    this->adminUpdateLayout->addWidget(this->adminUpdateSizeLabel, 0, 0);
    this->adminUpdateLayout->addWidget(this->adminUpdateSizeLine, 0, 1);
    this->adminUpdateLayout->addWidget(this->adminUpdateColorLabel, 1, 0);
    this->adminUpdateLayout->addWidget(this->adminUpdateColorLine, 1, 1);
    this->adminUpdateLayout->addWidget(this->adminUpdatePriceLabel, 2, 0);
    this->adminUpdateLayout->addWidget(this->adminUpdatePriceLine, 2, 1);
    this->adminUpdateLayout->addWidget(this->adminUpdateQuantityLabel, 3, 0);
    this->adminUpdateLayout->addWidget(this->adminUpdateQuantityLine, 3, 1);
    this->adminUpdateLayout->addWidget(this->adminUpdatePhotoLabel, 4, 0);
    this->adminUpdateLayout->addWidget(this->adminUpdatePhotoLine, 4, 1);
    this->adminUpdateLayout->addWidget(this->adminUpdateButton, 5, 0, 1, 2);

    // add the elements to the undo/redo layout
    this->adminUndoRedoLayout->addWidget(this->adminUndoButton, 0, 0);
    this->adminUndoRedoLayout->addWidget(this->adminRedoButton, 0, 1);

    // add the layout to the admin window
    this->adminWindow->setLayout(this->adminLayout);

    // style the admin form
    this->adminWindow->setWindowTitle("Administrator Window");
    this->adminWindow->setFixedSize(450, 475);


    // ------------------ user window ------------------

    // user layout
    this->userLayout = new QHBoxLayout();
    this->userOutputLayout = new QVBoxLayout();
    this->userInputLayout = new QVBoxLayout();
    this->userNextLayout = new QGridLayout();
    this->userViewLayout = new QGridLayout();
    this->userBasketTotalLayout = new QGridLayout();
    this->userEmptyBasketLayout = new QGridLayout();

    // user output elements
    this->userList = new QListWidget();
    this->userOutputLine = new QLineEdit();
    this->userOutputLine->setReadOnly(true);

    // user buttons
    this->userAddToBsketButton = new QPushButton("Add To Basket");
    this->userNextButton = new QPushButton("Next");
    this->userEmptyBasketButton = new QPushButton("Empty Basket");
    this->userOpenButton = new QPushButton("Open");
    this->userTableViewButton = new QPushButton("View Basket Table");
    this->userBackButton = new QPushButton("Back");

    // user next input fields
    this->userNextSizeLine = new QLineEdit();
    // user next labels
    this->userNextSizeLabel = new QLabel("Size");

    // user view output fields
    this->userBasketTotalLine = new QLineEdit();
    this->userBasketTotalLine->setReadOnly(true);
    this->userViewSizeLine = new QLineEdit();
    this->userViewSizeLine->setReadOnly(true);
    this->userViewColorLine = new QLineEdit();
    this->userViewColorLine->setReadOnly(true);
    this->userViewPriceLine = new QLineEdit();
    this->userViewPriceLine->setReadOnly(true);
    this->userViewQuantityLine = new QLineEdit();
    this->userViewQuantityLine->setReadOnly(true);
    this->userViewPhotoLine = new QLineEdit();
    this->userViewPhotoLine->setReadOnly(true);
    // user view labels
    this->userBasketTotalLabel = new QLabel("Basket Total");
    this->userViewSizeLabel = new QLabel("Size");
    this->userViewColorLabel = new QLabel("Color");
    this->userViewPriceLabel = new QLabel("Price");
    this->userViewQuantityLabel = new QLabel("Quantity");
    this->userViewPhotoLabel = new QLabel("Photo");

    // add the elements to the user layout
    this->userLayout->addLayout(this->userOutputLayout);
    this->userLayout->addLayout(this->userInputLayout);
    this->userLayout->addLayout(this->userViewLayout);

    // add elements to the output layout
    this->userOutputLayout->addWidget(this->userList);
    this->userOutputLayout->addWidget(this->userOutputLine);

    // add elements to the input layout
    this->userInputLayout->addLayout(this->userBasketTotalLayout);
    this->userInputLayout->addLayout(this->userNextLayout);
    this->userInputLayout->addWidget(this->userAddToBsketButton);
    this->userInputLayout->addLayout(this->userEmptyBasketLayout);
    this->userInputLayout->addWidget(this->userOpenButton);
    this->userInputLayout->addWidget(this->userTableViewButton);
    this->userInputLayout->addWidget(this->userBackButton);


    // add elements to the basket total layout
    this->userBasketTotalLayout->addWidget(this->userBasketTotalLabel, 0, 0);
    this->userBasketTotalLayout->addWidget(this->userBasketTotalLine, 0, 1);

    // add elements to the next layout
    this->userNextLayout->addWidget(this->userNextSizeLabel, 0, 0);
    this->userNextLayout->addWidget(this->userNextSizeLine, 0, 1);
    this->userNextLayout->addWidget(this->userNextButton, 1, 0, 1, 2);

    // add elements to the filter layout
    this->userEmptyBasketLayout->addWidget(this->userEmptyBasketButton, 1, 0, 1, 2);

    // add elements to the view layout
    this->userViewLayout->addWidget(this->userViewPhotoLabel, 0, 0);
    this->userViewLayout->addWidget(this->userViewPhotoLine, 0, 1);
    this->userViewLayout->addWidget(this->userViewSizeLabel, 1, 0);
    this->userViewLayout->addWidget(this->userViewSizeLine, 1, 1);
    this->userViewLayout->addWidget(this->userViewColorLabel, 2, 0);
    this->userViewLayout->addWidget(this->userViewColorLine, 2, 1);
    this->userViewLayout->addWidget(this->userViewPriceLabel, 3, 0);
    this->userViewLayout->addWidget(this->userViewPriceLine, 3, 1);
    this->userViewLayout->addWidget(this->userViewQuantityLabel, 4, 0);
    this->userViewLayout->addWidget(this->userViewQuantityLine, 4, 1);

    // add the layout to the user window
    this->userWindow->setLayout(this->userLayout);

    // style the user form
    this->userWindow->setWindowTitle("User Window");
    this->userWindow->setFixedSize(800, 500);
    this->userViewPhotoLine->setFixedWidth(250);

    // ------------------ connections ------------------

    // form selection
    connect(this->adminButton, &QPushButton::clicked, this, &GUI::showAdminWindow);
    connect(this->userCSVButton, &QPushButton::clicked, this, &GUI::setBasketToCSV);
    connect(this->userHTMLButton, &QPushButton::clicked, this, &GUI::setBasketToHTML);

    // admin commands
    connect(this->adminAddButton, &QPushButton::clicked, this, &GUI::addCoat);
    connect(this->adminRemoveButton, &QPushButton::clicked, this, &GUI::removeCoat);
    connect(this->adminUpdateButton, &QPushButton::clicked, this, &GUI::updateCoat);
    connect(this->adminUndoButton, &QPushButton::clicked, this, &GUI::onUndo);
    connect(this->adminRedoButton, &QPushButton::clicked, this, &GUI::onRedo);
    connect(this->adminBackButton, &QPushButton::clicked, this, &GUI::showEntryWindow);

    // Create Undo shortcut (Ctrl+Z)
    auto* undoShortcut = new QShortcut(QKeySequence("Ctrl+Z"), this->adminWindow);
    connect(undoShortcut, &QShortcut::activated, this, &GUI::onUndo);

    // Create Redo shortcut (Ctrl+Y)
    auto* redoShortcut = new QShortcut(QKeySequence("Ctrl+Y"), this->adminWindow);
    connect(redoShortcut, &QShortcut::activated, this, &GUI::onRedo);

    // user commands
    connect(this->userNextButton, &QPushButton::clicked, this, &GUI::userNext);
    connect(this->userAddToBsketButton, &QPushButton::clicked, this, &GUI::userAddToBasket);
    connect(this->userEmptyBasketButton, &QPushButton::clicked, this, &GUI::userEmptyBasket);
    connect(this->userOpenButton, &QPushButton::clicked, this, &GUI::userOpen);
    connect(this->userTableViewButton, &QPushButton::clicked, this, &GUI::showBasketWindow);
    connect(this->userBackButton, &QPushButton::clicked, this, &GUI::showEntryWindow);

    showEntryWindow();
}

GUI::~GUI() {
    delete ui;
}

void GUI::showEntryWindow() const {
    this->userList->clear();

    this->userWindow->setVisible(false);
    this->adminWindow->setVisible(false);
    this->entryWindow->setVisible(true);
}

void GUI::showAdminWindow() {
    this->updateAdminList();
    this->adminOutputLine->clear();
    this->clearAdminInputFields();
    this->userWindow->setVisible(false);
    this->entryWindow->setVisible(false);
    this->adminWindow->setVisible(true);
}

void GUI::showUserWindow() {
    this->currentCoatIndex = 0;

    this->userWindow->setVisible(true);
    this->adminWindow->setVisible(false);
    this->entryWindow->setVisible(false);

    this->clearUserInputFields();
    this->updateUserList();
}


void GUI::updateAdminList() {
    this->adminList->clear();
    for (auto &coat : this->service.getAllTrenchCoats()) {
        this->adminList->addItem(QString::fromStdString(coat.toString()));
    }
}

void GUI::updateUserList() {
    this->userList->clear();
    vector<TrenchCoat> coats = this->userService.getAllTrenchCoats();

    for (auto &coat : this->userService.getAllTrenchCoats()) {
        this->userList->addItem(QString::fromStdString(coat.toString()));
        this->userService.setTotalBasketPrice(this->userService.getTotalBasketPrice() + coat.GetPrice());
    }

    this->userBasketTotalLine->setText(QString::fromStdString(to_string(this->userService.getTotalBasketPrice())));
}

void GUI::clearAdminInputFields() const {
    this->adminAddSizeLine->clear();
    this->adminAddColorLine->clear();
    this->adminAddPriceLine->clear();
    this->adminAddQuantityLine->clear();
    this->adminAddPhotoLine->clear();
    this->adminRemoveSizeLine->clear();
    this->adminRemoveColorLine->clear();
    this->adminUpdateSizeLine->clear();
    this->adminUpdateColorLine->clear();
    this->adminUpdatePriceLine->clear();
    this->adminUpdateQuantityLine->clear();
    this->adminUpdatePhotoLine->clear();
}

void GUI::clearUserInputFields() const {
    this->userNextSizeLine->clear();
    this->userOutputLine->clear();
    this->userViewSizeLine->clear();
    this->userViewColorLine->clear();
    this->userViewPriceLine->clear();
    this->userViewQuantityLine->clear();
    this->userViewPhotoLine->clear();
}

void GUI::addCoat() {
    try {
        auto *size = new char[this->adminAddSizeLine->text().toStdString().length() + 1];
        strcpy(size, this->adminAddSizeLine->text().toStdString().c_str());
        auto *color = new char[this->adminAddColorLine->text().toStdString().length() + 1];
        strcpy(color, this->adminAddColorLine->text().toStdString().c_str());
        const double price = this->adminAddPriceLine->text().toDouble();
        const int quantity = this->adminAddQuantityLine->text().toInt();
        auto *photo = new char[this->adminAddPhotoLine->text().toStdString().length() + 1];
        strcpy(photo, this->adminAddPhotoLine->text().toStdString().c_str());

        this->saveUndoRepo();

        this->service.addTrenchCoat(size, color, price, quantity, photo);

        this->updateAdminList();
        this->adminOutputLine->setText("Coat added successfully!");
    }
    catch (CustomException &exception) {
        this->adminOutputLine->setText(QString::fromStdString(exception.what()));
    }

    this->clearAdminInputFields();
}

void GUI::removeCoat() {
    try {
        auto *size = new char[this->adminRemoveSizeLine->text().toStdString().length() + 1];
        strcpy(size, this->adminRemoveSizeLine->text().toStdString().c_str());
        auto *color = new char[this->adminRemoveColorLine->text().toStdString().length() + 1];
        strcpy(color, this->adminRemoveColorLine->text().toStdString().c_str());

        this->saveUndoRepo();

        this->service.removeTrenchCoat(size, color);

        this->updateAdminList();
        this->adminOutputLine->setText("Coat removed successfully!");
    }
    catch (CustomException &exception) {
        this->adminOutputLine->setText(QString::fromStdString(exception.what()));
    }

    this->clearAdminInputFields();
}

void GUI::updateCoat() {
    try {
        auto *size = new char[this->adminUpdateSizeLine->text().toStdString().length() + 1];
        strcpy(size, this->adminUpdateSizeLine->text().toStdString().c_str());
        auto *color = new char[this->adminUpdateColorLine->text().toStdString().length() + 1];
        strcpy(color, this->adminUpdateColorLine->text().toStdString().c_str());
        const double price = this->adminUpdatePriceLine->text().toDouble();
        const int quantity = this->adminUpdateQuantityLine->text().toInt();
        auto *photo = new char[this->adminUpdatePhotoLine->text().toStdString().length() + 1];
        strcpy(photo, this->adminUpdatePhotoLine->text().toStdString().c_str());

        this->saveUndoRepo();

        this->service.updateTrenchCoat(size, color, price, quantity, photo);

        this->updateAdminList();
        this->adminOutputLine->setText("Coat updated successfully!");
    }
    catch (CustomException &exception) {
        this->adminOutputLine->setText(QString::fromStdString(exception.what()));
    }

    this->clearAdminInputFields();
}

void GUI::onUndo() {
    if(this->undoStack.empty()) {
        this->adminOutputLine->setText("No more undos!");
        return;
    }

    Repository *repository = this->undoStack.top(); // get the value with top
    this->undoStack.pop(); // remove the value with pop

    saveRedoRepo();

    this->service.setRepository(repository);

    this->updateAdminList();
}

void GUI::onRedo() {
    if(this->redoStack.empty()) {
        this->adminOutputLine->setText("No more redos!");
        return;
    }

    saveUndoRepo();

    Repository *repository = this->redoStack.top(); // get the value with top
    this->redoStack.pop(); // remove the value with pop

    this->service.setRepository(repository);

    this->updateAdminList();
}

void GUI::saveUndoRepo() {
    Repository *tempRepo = this->service.getRepository();
    this->undoStack.push(tempRepo);
}

void GUI::saveRedoRepo() {
    Repository *tempRepo = this->service.getRepository();
    this->redoStack.push(tempRepo);
}

void GUI::setBasketToCSV() {
    if(csvRepo.GetSize() == 0)
        csvRepo.ReadFromFile();
    const Service user(csvRepo);
    userService = user;

    this->showUserWindow();
}

void GUI::setBasketToHTML() {
    Service user(htmlRepo);
    if(htmlRepo.GetSize() == 0)
        htmlRepo.ReadFromFile();
    userService = user;

    this->showUserWindow();
}

void GUI::userNext() {
    auto *size = new char[this->userNextSizeLine->text().toStdString().length() + 1];
    strcpy(size, this->userNextSizeLine->text().toStdString().c_str());

    vector<TrenchCoat> trenchCoats = this->service.getFilteredBySizeTrenchCoats(size);
    this->coatsStock = trenchCoats;
    if (trenchCoats.empty()) {
        this->userOutputLine->setText("No more coats with the given size!");
        return;
    }

    if (this->currentCoatIndex >= trenchCoats.size()) {
        this->currentCoatIndex = 0;
    }

    TrenchCoat coat = trenchCoats[this->currentCoatIndex];

    this->userViewSizeLine->setText(QString::fromStdString(coat.GetSize()));
    this->userViewColorLine->setText(QString::fromStdString(coat.GetColor()));
    this->userViewPriceLine->setText(QString::number(coat.GetPrice()));
    this->userViewQuantityLine->setText(QString::number(coat.GetQuantity()));
    this->userViewPhotoLine->setText(QString::fromStdString(coat.GetPhotograph()));

    this->currentCoatIndex++;
    if (this->currentCoatIndex == trenchCoats.size()) {
        this->currentCoatIndex = 0;
    }
}

void GUI::userAddToBasket() {
    try {
        int index = this->currentCoatIndex;
        if (index != 0)
            index--;
        TrenchCoat coat = this->coatsStock[index];
        const string size = coat.GetSize();
        const string color = coat.GetColor();
        const double price = coat.GetPrice();
        const int quantity = coat.GetQuantity();
        const string photo = coat.GetPhotograph();
        this->userService.addTrenchCoat(size, color, price, quantity, photo);
        this->userService.setTotalBasketPrice(this->userService.getTotalBasketPrice() + coat.GetPrice());
        this->updateUserList();
        this->userNext();
        this->userOutputLine->setText("Coat added to basket successfully!");
    }
    catch (CustomException &exception) {
        this->userOutputLine->setText(QString::fromStdString(exception.what()));
    }
}

void GUI::userEmptyBasket() {
    vector<TrenchCoat> trenchCoats = this->userService.getAllTrenchCoats();
    for (auto &coat : trenchCoats) {
        this->userService.removeTrenchCoat(coat.GetSize(), coat.GetColor());
    }
    this->userService.setTotalBasketPrice(0);
    this->updateUserList();
    this->userOutputLine->setText("Basket emptied successfully!");
}

void GUI::userOpen() {
    this->updateUserList();

    if (this->userService.getAllTrenchCoats().empty()) {
        this->userOutputLine->setText(QString::fromStdString("The basket is empty!"));
        return;
    }

    try {
        this->userService.openShoppingBasketInApplication();
        this->userOutputLine->setText(QString::fromStdString("Basket opened successfully!"));
    } catch (CustomException &exception) {
        this->userOutputLine->setText(QString::fromStdString(exception.what()));
    }
}

void GUI::showBasketWindow() {
    // Create a new window for displaying the basket
    auto basketWindow = new QWidget();
    basketWindow->setWindowTitle("Shopping Basket");
    basketWindow->setFixedSize(600, 400);

    // Create a table view and set the custom model
    auto *tableView = new QTableView(basketWindow);
    tableView->setModel(new BasketModel(userService.getAllTrenchCoats(), this));

    // Create a layout for the window and add the table view to it
    auto *layout = new QVBoxLayout();
    layout->addWidget(tableView);
    basketWindow->setLayout(layout);

    // Show the basket window
    basketWindow->show();
}

void GUI::paintEvent(QPaintEvent *event) {
    QPainter painter(this);

    int coatsUnder200DolarsCount = 0;
    int coatsOver200DolarsCount = 0;
    for (auto &coat : this->service.getAllTrenchCoats()) {
        if (coat.GetPrice() < 200) {
            coatsUnder200DolarsCount++;
        } else {
            coatsOver200DolarsCount++;
        }
    }
    int coatsUnder200DolarsAngle = coatsUnder200DolarsCount * 360 / this->service.getAllTrenchCoats().size();
    int coatsOver200DolarsAngle = 360 - coatsUnder200DolarsAngle;

    QRectF size = QRectF(82, 50, this->width() - 160, this->width() - 160);

    painter.setBrush(Qt::red);
    painter.drawPie(size, 0, coatsUnder200DolarsAngle * 16);
    painter.setBrush(Qt::blue);
    painter.drawPie(size, coatsUnder200DolarsAngle * 16, coatsOver200DolarsAngle * 16);

    /// Draw legend
    painter.setBrush(Qt::red);
    painter.drawRect(10, 20, 20, 20);
    painter.setBrush(Qt::blue);
    painter.drawRect(10, 50, 20, 20);
    painter.setBrush(Qt::black);
    painter.drawText(40, 35, "Coats under 200$");
    painter.drawText(40, 65, "Coats over 200$");
}

