#include "MainWindow.h"
#include "ui_MainWindow.h"
#include "DialogWelcome.h"
#include "DialogSelectFolder.h"
#include <QDebug>
#include <QTimer>

MainWindow::MainWindow(QWidget *parent)
  : QMainWindow(parent)
  , ui(new Ui::MainWindow)
{
  ui->setupUi(this);

  DialogWelcome dlg;
  if (dlg.exec() != QDialog::Accepted)
  {
    QTimer::singleShot(0, this, SLOT(close()));
    return;
  }

  DialogSelectFolder dlgSelect;
  if (dlgSelect.exec() != QDialog::Accepted)
  {
    QTimer::singleShot(0, this, SLOT(close()));
    return;
  }
}

MainWindow::~MainWindow()
{
  delete ui;
}

