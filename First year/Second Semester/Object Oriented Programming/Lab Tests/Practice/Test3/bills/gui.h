#ifndef GUI_H
#define GUI_H

#include <QWidget>

#include "service/service.h"
#include "domain/bill.h"


QT_BEGIN_NAMESPACE
namespace Ui { class GUI; }
QT_END_NAMESPACE

class GUI : public QWidget {
Q_OBJECT

public:
    explicit GUI(QWidget *parent = nullptr, Service service = Service());
    ~GUI() override;

private:
    Ui::GUI *ui;

    Service service;

    void populateList() const;
    void filterByUnpaidOrPaid() const;
    void calculateTotal() const;
    void addBill() const;
};


#endif //GUI_H
