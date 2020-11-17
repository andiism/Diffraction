import QtQuick 2.13
import QtQuick.Controls 2.13
import QtTest 1.14

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

Item {
    id: root


    Column {
        anchors.centerIn: parent
        spacing: EaStyle.Sizes.fontPixelSize * 2.5

        // Application logo, name and version
        Column {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 0

            // Application logo
            Image {
                source: ExGlobals.Constants.appLogo
                anchors.horizontalCenter: parent.horizontalCenter
                width: EaStyle.Sizes.fontPixelSize * 6
                fillMode: Image.PreserveAspectFit
                antialiasing: true
            }

            // Application name
            Row {
                property var fontFamily: EaStyle.Fonts.secondCondensedFontFamily
                property var fontPixelSize: EaStyle.Sizes.fontPixelSize * 4

                anchors.horizontalCenter: parent.horizontalCenter

                EaElements.Label {
                    font.family: parent.fontFamily
                    font.pixelSize: parent.fontPixelSize
                    font.weight: Font.ExtraLight
                    text: ExGlobals.Constants.appPrefixName
                }
                EaElements.Label {
                    font.family: parent.fontFamily
                    font.pixelSize: parent.fontPixelSize
                    text: ExGlobals.Constants.appSuffixName
                }
            }

            // Application version
            EaElements.Label {
                anchors.horizontalCenter: parent.horizontalCenter
                font.family: EaStyle.Fonts.secondExpandedFontFamily
                text: qsTr("Version %1 (%2)".arg(ExGlobals.Constants.appVersion).arg(ExGlobals.Constants.appDate))
            }
        }

        // Start button
        EaElements.SideBarButton {
            id: startButton
            width: EaStyle.Sizes.fontPixelSize * 15
            anchors.horizontalCenter: parent.horizontalCenter
            fontIcon: "rocket"
            text: qsTr("Start")
            onClicked: {
                ExGlobals.Variables.projectPageEnabled = true
                ExGlobals.Variables.projectTabButton.toggle()
            }
            Component.onCompleted: ExGlobals.Variables.startButton = startButton
        }

        // Links
        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: EaStyle.Sizes.fontPixelSize * 3

            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    enabled: false
                    text: qsTr("About %1".arg(ExGlobals.Constants.appName))
                }
                EaElements.Button {
                    enabled: false
                    text: qsTr("Online documentation")
                }
                EaElements.Button {
                    enabled: false
                    text: qsTr("Get in touch online")
                }
            }

            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    id: tutorial1Button
                    enabled: false
                    text: qsTr("Tutorial 1") + ": " + qsTr("Data fitting")
                    onPressed: {
                        runTutorial1()
                        setRootFocusTimer.start()
                    }
                }
                EaElements.Button {
                    id: tutorial2Button
                    text: qsTr("Tutorial 2") + ": " + qsTr("Data simulation")
                    onPressed: {
                        runTutorial2()
                        setRootFocusTimer.start()
                    }
                }
                EaElements.Button {
                    id: tutorial3Button
                    text: qsTr("Tutorial 3") + ": " + qsTr("App settings")
                    onPressed: {
                        runTutorial3()
                        setRootFocusTimer.start()
                    }
                }
            }
        }

    }

    // Remote controller for tutorials

    EaElements.RemoteController {
        id: rc
    }

    Timer {
        id: quitTimer
        interval: 1000
        onTriggered: {
            print("* closing app")
            Qt.quit()
        }
    }

    Timer {
        id: runTutorialTimer
        interval: 1000
        onTriggered: runTutorial2()
    }

    Timer {
        id: setRootFocusTimer
        interval: 100
        onTriggered: {
            tutorial1Button.enabled = !tutorial1Button.enabled
            tutorial1Button.enabled = !tutorial1Button.enabled
            tutorial2Button.enabled = !tutorial2Button.enabled
            tutorial2Button.enabled = !tutorial2Button.enabled
            tutorial3Button.enabled = !tutorial3Button.enabled
            tutorial3Button.enabled = !tutorial3Button.enabled
            root.forceActiveFocus()
        }
    }


    Component.onCompleted: {
        if (EaGlobals.Variables.isTestMode) {
            print('DEBUG MODE')
            runTutorialTimer.start()
        }
    }

    // Tutorials related logic

    function startSavingScreenshots() {
        if (EaGlobals.Variables.isTestMode) {
            EaGlobals.Variables.saveScreenshotsRunning = true
        }
    }

    function endSavingScreenshots() {
        if (EaGlobals.Variables.isTestMode) {
            EaGlobals.Variables.saveScreenshotsRunning = false
            quitTimer.start()
        }
    }

    function runTutorial1() {
        print("* run Tutorial 1")

        startSavingScreenshots()
        rc.wait(1000)
        rc.posToCenter()
        rc.show()

        rc.mouseClick(ExGlobals.Variables.startButton)
        rc.mouseClick(ExGlobals.Variables.createProjectButton)
        rc.mouseClick(ExGlobals.Variables.sampleTabButton)
        rc.mouseClick(ExGlobals.Variables.addNewSampleButton)
        rc.mouseClick(ExGlobals.Variables.sampleParametersGroup)

        rc.mouseClick(ExGlobals.Variables.amplitudeTextInput)
        rc.hide()
        rc.keyClick(Qt.Key_Right)
        rc.clearText(6)
        rc.typeText("2.1234")
        rc.keyClick(Qt.Key_Enter)
        rc.show()

        rc.mouseClick(ExGlobals.Variables.periodTextInput)
        rc.hide()
        rc.keyClick(Qt.Key_Right)
        rc.clearText(1)
        rc.typeText("6")
        rc.keyClick(Qt.Key_Enter)
        rc.show()

        rc.wait(2000)

        rc.mouseClick(ExGlobals.Variables.experimentTabButton)
        rc.mouseClick(ExGlobals.Variables.generateMeasuredDataButton)

        rc.wait(1000)

        rc.mouseClick(ExGlobals.Variables.analysisTabButton)
        rc.mouseClick(ExGlobals.Variables.xShiftFitCheckBox)

        rc.mouseClick(ExGlobals.Variables.xShiftValueTextInput)
        rc.hide()
        rc.keyClick(Qt.Key_Right)
        rc.keyClick(Qt.Key_Right)
        rc.keyClick(Qt.Key_Right)
        rc.keyClick(Qt.Key_Right)
        rc.clearText(6)
        rc.typeText("-0.3")
        rc.keyClick(Qt.Key_Enter)
        rc.show()

        rc.mouseClick(ExGlobals.Variables.startFittingButton)
        rc.mouseClick(ExGlobals.Variables.xShiftFitCheckBox)
        rc.mouseClick(ExGlobals.Variables.startFittingButton)

        rc.wait(1000)

        rc.hide()
        rc.wait(1000)
        endSavingScreenshots()
    }

    function runTutorial2() {
        print("* run Tutorial 2")

        // Start

        startSavingScreenshots()
        rc.wait(1000)
        rc.posToCenter()
        rc.show()

        // Home Tab

        rc.mouseClick(ExGlobals.Variables.startButton)

        // Project Tab

        rc.mouseClick(ExGlobals.Variables.createProjectButton)

        // Sample Tab

        rc.mouseClick(ExGlobals.Variables.sampleTabButton)

        rc.mouseClick(ExGlobals.Variables.setNewSampleManuallyButton)

        rc.mouseClick(ExGlobals.Variables.symmetryGroup, 15)
        rc.mouseClick(ExGlobals.Variables.cellLengthALabel)
        rc.hide()
        rc.keyClick(Qt.Key_Right)
        rc.keyClick(Qt.Key_Right)
        rc.clearText(4)
        rc.typeText("4.55")
        rc.keyClick(Qt.Key_Enter)
        rc.show()

        rc.mouseClick(ExGlobals.Variables.atomsGroup, 15)
        rc.mouseClick(ExGlobals.Variables.appendNewAtomButton)

        rc.wait(1000)

        // Experiment Tab

        rc.mouseClick(ExGlobals.Variables.experimentTabButton)

        rc.mouseClick(ExGlobals.Variables.continueWithoutExperimentDataButton)

        // Analysis Tab

        rc.mouseClick(ExGlobals.Variables.analysisTabButton)
        rc.wait(1000)
        rc.mouseClick(ExGlobals.Variables.analysisAdvancedControlsTabButton)
        // CFML
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        const x_pos = undefined
        let y_pos = EaStyle.Sizes.comboBoxHeight * 1.5
        rc.mouseClick(ExGlobals.Variables.calculatorSelector, x_pos, y_pos)
        rc.wait(1000)
        // GSAS
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        y_pos = EaStyle.Sizes.comboBoxHeight * 2.5
        rc.mouseClick(ExGlobals.Variables.calculatorSelector, x_pos, y_pos)
        rc.wait(1000)
        // CrysPy
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        rc.mouseClick(ExGlobals.Variables.analysisBasicControlsTabButton)

        // End

        rc.hide()
        rc.wait(1000)
        endSavingScreenshots()
    }

    function runTutorial3() {
        print("* run Tutorial 3")

        startSavingScreenshots()
        rc.wait(1000)
        rc.posToCenter()
        rc.show()

        rc.mouseClick(ExGlobals.Variables.preferencesButton)
        rc.mouseClick(ExGlobals.Variables.themeSelector)

        const x_pos = undefined
        let y_pos = !EaStyle.Colors.isDarkTheme ? EaStyle.Sizes.comboBoxHeight * 1.5 : undefined
        rc.mouseClick(ExGlobals.Variables.themeSelector, x_pos, y_pos)

        rc.wait(1000)

        rc.mouseClick(ExGlobals.Variables.themeSelector)
        y_pos = !EaStyle.Colors.isDarkTheme ? EaStyle.Sizes.comboBoxHeight * 1.5 : undefined
        rc.mouseClick(ExGlobals.Variables.themeSelector, x_pos, y_pos)

        rc.wait(1000)
        rc.keyClick(Qt.Key_Escape)

        rc.wait(1000)

        rc.hide()
        rc.wait(1000)
        endSavingScreenshots()
    }

}
