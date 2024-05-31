#ifndef GUI_H
#define GUI_H

#include <qlistwidget.h>
#include <QApplication>
#include <QWidget>
#include <qlineedit.h>
#include <qlabel.h>
#include "headers/service/service.h"
#include "headers/utilities/exceptions.h"
#include <qlayout.h>
#include <QPushButton>
#include <QPainter>
#include <stack>
#include <QShortcut>
#include <QKeySequence>
#include "BasketModel.h"
#include <QTableView>
#include "gui.h"


QT_BEGIN_NAMESPACE
namespace Ui { class GUI; }
QT_END_NAMESPACE

class GUI : public QWidget {
Q_OBJECT

public:
    explicit GUI(QWidget *parent = nullptr, const Service &service = Service());
    ~GUI() override;

private:
    Ui::GUI *ui;
    QWidget *entryWindow;
    QWidget *adminWindow;
    QWidget *userWindow;

    Service service;
    stack<Repository*> undoStack;
    stack<Repository*> redoStack;

    Repository userRepo;
    CSVRepository csvRepo{"../data/shoppingBasket.csv"};
    HTMLRepository htmlRepo{"../data/shoppingBasket.html"};
    Service userService{userRepo};
    vector<TrenchCoat> coatsStock;

    int currentCoatIndex{};

    // ----------Entry layout----------
    QGridLayout *entryLayout;
    QPushButton *adminButton;
    QPushButton *userCSVButton;
    QPushButton *userHTMLButton;

    // ----------Admin layout----------
    QHBoxLayout *adminLayout;
    QVBoxLayout *adminOutputLayout;
    QVBoxLayout *adminCommandsLayout;
    QGridLayout *adminAddLayout;
    QGridLayout *adminRemoveLayout;
    QGridLayout *adminUpdateLayout;
    QGridLayout *adminUndoRedoLayout;

    // admin widget list
    QListWidget *adminList;
    // admin output text box for messages
    QLineEdit *adminOutputLine;

    // admin buttons
    QPushButton *adminAddButton;
    QPushButton *adminRemoveButton;
    QPushButton *adminUpdateButton;
    QPushButton *adminBackButton;
    QPushButton *adminUndoButton;
    QPushButton *adminRedoButton;

    // admin add input fields
    QLineEdit *adminAddSizeLine;
    QLineEdit *adminAddColorLine;
    QLineEdit *adminAddPriceLine;
    QLineEdit *adminAddQuantityLine;
    QLineEdit *adminAddPhotoLine;
    // admin add labels
    QLabel *adminAddSizeLabel;
    QLabel *adminAddColorLabel;
    QLabel *adminAddPriceLabel;
    QLabel *adminAddQuantityLabel;
    QLabel *adminAddPhotoLabel;

    // admin remove input fields
    QLineEdit *adminRemoveSizeLine;
    QLineEdit *adminRemoveColorLine;
    // admin remove labels
    QLabel *adminRemoveSizeLabel;
    QLabel *adminRemoveColorLabel;

    // admin update input fields
    QLineEdit *adminUpdateSizeLine;
    QLineEdit *adminUpdateColorLine;
    QLineEdit *adminUpdatePriceLine;
    QLineEdit *adminUpdateQuantityLine;
    QLineEdit *adminUpdatePhotoLine;
    // admin update labels
    QLabel *adminUpdateSizeLabel;
    QLabel *adminUpdateColorLabel;
    QLabel *adminUpdatePriceLabel;
    QLabel *adminUpdateQuantityLabel;
    QLabel *adminUpdatePhotoLabel;

    // ----------User layout----------
    QHBoxLayout *userLayout;
    QVBoxLayout *userOutputLayout;
    QVBoxLayout *userInputLayout;
    QGridLayout *userNextLayout;
    QGridLayout *userEmptyBasketLayout;
    QGridLayout *userViewLayout;
    QGridLayout *userBasketTotalLayout;

    // user widget list
    QListWidget *userList;
    // user output text box for messages
    QLineEdit *userOutputLine;

    // user buttons
    QPushButton *userNextButton;
    QPushButton *userAddToBsketButton;
    QPushButton *userEmptyBasketButton;
    QPushButton *userOpenButton;
    QPushButton *userBackButton;
    QPushButton *userTableViewButton;

    // user input fields
    QLineEdit *userNextSizeLine;
    // user labels
    QLabel *userNextSizeLabel;

    // user view outputs fields
    QLineEdit *userBasketTotalLine;
    QLineEdit *userViewSizeLine;
    QLineEdit *userViewColorLine;
    QLineEdit *userViewPriceLine;
    QLineEdit *userViewQuantityLine;
    QLineEdit *userViewPhotoLine;
    // user view labels
    QLabel *userBasketTotalLabel;
    QLabel *userViewSizeLabel;
    QLabel *userViewColorLabel;
    QLabel *userViewPriceLabel;
    QLabel *userViewQuantityLabel;
    QLabel *userViewPhotoLabel;

    void showEntryWindow() const;
    void showAdminWindow();
    void showUserWindow();
    void updateAdminList();
    void updateUserList();
    void clearAdminInputFields() const;
    void clearUserInputFields() const;

    void addCoat();
    void removeCoat();
    void updateCoat();
    void onUndo();
    void onRedo();
    void saveUndoRepo();
    void saveRedoRepo();

    void setBasketToCSV();
    void setBasketToHTML();

    void userNext();
    void userAddToBasket();
    void userEmptyBasket();
    void userOpen();
    void showBasketWindow();

protected:
    void paintEvent(QPaintEvent *event) override;
};


#endif //GUI_H
