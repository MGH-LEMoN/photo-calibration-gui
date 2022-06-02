#include "DialogSelectFolder.h"
#include "ui_DialogSelectFolder.h"

DialogSelectFolder::DialogSelectFolder(QWidget *parent) :
  QDialog(parent),
  ui(new Ui::DialogSelectFolder)
{
  ui->setupUi(this);
}

DialogSelectFolder::~DialogSelectFolder()
{
  delete ui;
}

void DialogSelectFolder::OnButtonInputPath()
{

}

void DialogSelectFolder::OnButtonOutputPath()
{

}

void DialogSelectFolder::OnButtonRegister()
{

}

QString DialogSelectFolder::GetInputPath()
{
  return ui->lineEditPathInput->text().trimmed();
}

QString DialogSelectFolder::GetOutputPath()
{
  return ui->lineEditPathOutput->text().trimmed();
}

bool DialogSelectFolder::IsFourPoint()
{
  return ui->radioButton4Points->isChecked();
}
