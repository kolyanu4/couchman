# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Nov 18 13:31:04 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

import pkg_resources
from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 600)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralWidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.fileMenu = self.menubar.addMenu("File")
        self.quit_action = self.fileMenu.addAction('Quit')
        self.quit_action.setShortcut(QtGui.QKeySequence.Quit)
        self.ServersMenu = self.menubar.addMenu("Servers")
        self.add_server_action = self.ServersMenu.addAction("Add Server")
        self.add_server_action.setShortcut(QtGui.QKeySequence('Ctrl+A'))
        self.remove_server_action = self.ServersMenu.addAction("Remove Server")
        self.remove_server_action.setShortcut(QtGui.QKeySequence('Ctrl+R'))
        self.edit_server_action = self.ServersMenu.addAction("Edit Server")
        self.edit_server_action.setShortcut(QtGui.QKeySequence('Ctrl+E'))
        self.db_manager_action = self.ServersMenu.addAction("DB Manager")
        self.db_manager_action.setShortcut(QtGui.QKeySequence('Ctrl+D'))
        self.WindowsMenu = self.menubar.addMenu("Windows")
        self.workers_action = self.WindowsMenu.addAction("Workers")
        self.workers_action.setShortcut(QtGui.QKeySequence('Ctrl+K'))
        MainWindow.setMenuBar(self.menubar)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtGui.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tlw_servers = ServersList(self.layoutWidget)
        self.tlw_servers.setAlternatingRowColors(True)
        self.tlw_servers.setRootIsDecorated(False)
        self.tlw_servers.setUniformRowHeights(True)
        self.tlw_servers.setItemsExpandable(False)
        self.tlw_servers.setSortingEnabled(True)
        self.tlw_servers.setWordWrap(True)
        self.tlw_servers.setExpandsOnDoubleClick(False)
        self.tlw_servers.setObjectName("tlw_servers")
        self.verticalLayout_2.addWidget(self.tlw_servers)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout_3.setVerticalSpacing(10)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lbl_srv_group = QtGui.QLabel(self.layoutWidget1)
        self.lbl_srv_group.setObjectName("lbl_srv_group")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.lbl_srv_group)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lbl_srv_name = QtGui.QLabel(self.layoutWidget1)
        self.lbl_srv_name.setObjectName("lbl_srv_name")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.lbl_srv_name)
        self.label_4 = QtGui.QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lbl_srv_addres = QtGui.QLabel(self.layoutWidget1)
        self.lbl_srv_addres.setCursor(QtCore.Qt.PointingHandCursor)
        self.lbl_srv_addres.setMouseTracking(True)
        self.lbl_srv_addres.setTextFormat(QtCore.Qt.AutoText)
        self.lbl_srv_addres.setOpenExternalLinks(True)
        self.lbl_srv_addres.setObjectName("lbl_srv_addres")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.lbl_srv_addres)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lbl_status = QtGui.QLabel(self.layoutWidget1)
        self.lbl_status.setObjectName("lbl_status")
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.lbl_status)
        self.label_6 = QtGui.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lbl_period = QtGui.QLabel(self.layoutWidget1)
        self.lbl_period.setObjectName("lbl_period")
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.FieldRole, self.lbl_period)
        self.label_5 = QtGui.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbl_lastupdate = QtGui.QLabel(self.layoutWidget1)
        self.lbl_lastupdate.setObjectName("lbl_lastupdate")
        self.horizontalLayout_4.addWidget(self.lbl_lastupdate)
        self.btn_refresh_sel = QtGui.QToolButton(self.layoutWidget1)
        self.btn_refresh_sel.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_refresh_sel.setObjectName("btn_refresh_sel")
        self.horizontalLayout_4.addWidget(self.btn_refresh_sel)
        self.formLayout_3.setLayout(5, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.horizontalLayout_3.addLayout(self.formLayout_3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tlw_replications_label = QtGui.QLabel(self.layoutWidget1)
        self.tlw_replications_label.setObjectName("tlw_replications_label")
        self.tlw_replications_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.tlw_replications_label.setStyleSheet("QLabel { color : red; }")
        self.verticalLayout.addWidget(self.tlw_replications_label)
        self.tlw_replications = ServersList(self.layoutWidget1)
        self.tlw_replications.setAlternatingRowColors(True)
        self.tlw_replications.setRootIsDecorated(False)
        self.tlw_replications.setItemsExpandable(False)
        self.tlw_replications.setExpandsOnDoubleClick(False)
        self.tlw_replications.setObjectName("tlw_replications")
        self.verticalLayout.addWidget(self.tlw_replications)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_addtask = QtGui.QToolButton(self.layoutWidget1)
        self.btn_addtask.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_addtask.setObjectName("btn_addtask")
        self.horizontalLayout_2.addWidget(self.btn_addtask)
        self.btn_rmtask = QtGui.QToolButton(self.layoutWidget1)
        self.btn_rmtask.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_rmtask.setObjectName("btn_rmtask")
        self.horizontalLayout_2.addWidget(self.btn_rmtask)
        self.btn_starttask = QtGui.QToolButton(self.layoutWidget1)
        self.btn_starttask.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_starttask.setObjectName("btn_starttask")
        self.horizontalLayout_2.addWidget(self.btn_starttask)
        self.btn_start_con = QtGui.QToolButton(self.layoutWidget1)
        self.btn_start_con.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_start_con.setObjectName("btn_start_con")
        self.horizontalLayout_2.addWidget(self.btn_start_con)
        self.btn_stoptask = QtGui.QToolButton(self.layoutWidget1)
        self.btn_stoptask.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_stoptask.setObjectName("btn_stoptask")
        self.horizontalLayout_2.addWidget(self.btn_stoptask)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralWidget)
        self.actionAdd_Server = QtGui.QAction(MainWindow)
        self.actionAdd_Server.setObjectName("actionAdd_Server")
        self.actionRemove_Server = QtGui.QAction(MainWindow)
        self.actionRemove_Server.setObjectName("actionRemove_Server")
        self.revision = pkg_resources.get_distribution("couchman").version
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", ("Replication Manager - %s" % self.revision), None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Group:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_srv_group.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_srv_name.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Addres:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_srv_addres.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Status:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_status.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Update period: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_period.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Last update:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_lastupdate.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_refresh_sel.setText(QtGui.QApplication.translate("MainWindow", "Refresh now", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_addtask.setToolTip(QtGui.QApplication.translate("MainWindow", "Add replication record to persisted list", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_addtask.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_rmtask.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove replication record from persisted list", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_rmtask.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_starttask.setToolTip(QtGui.QApplication.translate("MainWindow", "Start persisted replication", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_starttask.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_start_con.setText(QtGui.QApplication.translate("MainWindow", "Start as continuous", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_stoptask.setToolTip(QtGui.QApplication.translate("MainWindow", "Stop runing replication", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_stoptask.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Server.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Server.setToolTip(QtGui.QApplication.translate("MainWindow", "Add new Server", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Server.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove_Server.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove_Server.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))

from list_prototype import ServersList
