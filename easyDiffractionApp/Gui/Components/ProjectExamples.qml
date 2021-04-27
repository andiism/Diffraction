import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    id: tableView

    defaultInfoText: qsTr("No Examples Available")

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.projectExamplesAsXml
        query: "/root/item"

        XmlRole { name: "name"; query: "name/string()" }
        XmlRole { name: "description"; query: "description/string()" }
        XmlRole { name: "path"; query: "path/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            id: indexColumn

            width: EaStyle.Sizes.fontPixelSize * 2.5

            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
            width: tableView.width
                   - indexColumn.width
                   - descriptionColumn.width
                   - uploadColumn.width
                   - EaStyle.Sizes.tableColumnSpacing * 3
                   - EaStyle.Sizes.borderThickness

            horizontalAlignment: Text.AlignLeft

            headerText: "Name"
            text: model.name
        }

        EaComponents.TableViewLabel {
            id: descriptionColumn

            width: EaStyle.Sizes.fontPixelSize * 25

            horizontalAlignment: Text.AlignLeft

            headerText: "Description"
            text: model.description
        }

        EaComponents.TableViewButton {
            id: uploadColumn

            fontIcon: "upload"
            ToolTip.text: qsTr("Load this example")

            onClicked: {
                const fileUrl = Qt.resolvedUrl(model.path)
                ExGlobals.Constants.proxy.loadProjectAs(fileUrl)

                ExGlobals.Variables.sampleLoaded = true

                ExGlobals.Variables.samplePageEnabled = true
                ExGlobals.Variables.experimentPageEnabled = true
                ExGlobals.Variables.projectCreated = true
                ExGlobals.Variables.analysisPageEnabled = true
                ExGlobals.Variables.summaryPageEnabled = true
            }

            Component.onCompleted: {
                if (model.name === 'PbSO4') {
                    ExGlobals.Variables.loadExampleProjectButton = this
                }
            }
        }
    }

}
