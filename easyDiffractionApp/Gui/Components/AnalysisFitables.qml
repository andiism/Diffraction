import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    id: table

    maxRowCountShow: 8

    // Table model

    model: XmlListModel {
        id: fitablesModel

        xml: ExGlobals.Constants.proxy.fitablesListAsXml

        query: "/root/item"

        XmlRole { name: "id"; query: "id/string()" }
        XmlRole { name: "number"; query: "number/number()" }
        XmlRole { name: "label"; query: "label/string()" }
        XmlRole { name: "value"; query: "value/number()" }
        XmlRole { name: "unit"; query: "unit/string()" }
        XmlRole { name: "error"; query: "error/number()" }
        XmlRole { name: "fit"; query: "fit/number()" }

        onStatusChanged: {
            if (status === XmlListModel.Ready) {
                storeCurrentParameter()
            }
        }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            id: numberColumn
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.number
        }

        EaComponents.TableViewLabel {
            id: labelColumn
            horizontalAlignment: Text.AlignLeft
            width: table.width -
                   (parent.children.length - 1) * EaStyle.Sizes.tableColumnSpacing -
                   numberColumn.width -
                   valueColumn.width -
                   unitColumn.width -
                   errorColumn.width -
                   useColumn.width
            headerText: "Label"
            text: formatLabel(model.index, model.label)
            textFormat: Text.RichText
        }

        EaComponents.TableViewTextInput {
            id: valueColumn
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Value"
            text: model.value.toFixed(4)
            onEditingFinished: editParameterValue(model.id, text)
        }

        EaComponents.TableViewLabel {
            id: unitColumn
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 2
            text: model.unit
            color: EaStyle.Colors.themeForegroundMinor
        }

        EaComponents.TableViewLabel {
            id: errorColumn
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Error  "
            text: model.error === 0.0 || model.error > 999999 ? "" : model.error.toFixed(4) + "  "
        }

        EaComponents.TableViewCheckBox {
            enabled: ExGlobals.Variables.experimentLoaded
            id: useColumn
            headerText: "Fit"
            checked: model.fit
        }

    }

    onCurrentIndexChanged: storeCurrentParameter()

    // Logic

    function storeCurrentParameter() {
        if (typeof model.get(currentIndex) === "undefined")
            return
        ExGlobals.Variables.currentParameterId = model.get(currentIndex).id
        ExGlobals.Variables.currentParameterValue = model.get(currentIndex).value
    }

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameterValue(id, parseFloat(value))
    }

    function formatLabel(index, label) {
        if (index < 0 || typeof label === "undefined")
            return ""

        // Modify current label
        label = label.replace("Uiso.Uiso", "Uiso")
        label = label.replace("fract_", "fract.")
        label = label.replace("length_", "length.")
        label = label.replace("angle_", "angle.")

        // Current label to list
        let list = label.split(".")
        const last = list.length - 1

        // Modify previous label to list
        let previousLabel = index > 0 ? fitablesModel.get(index - 1).label : ""
        previousLabel = previousLabel.replace("Uiso.Uiso", "Uiso")
        previousLabel = previousLabel.replace("fract_", "fract.")
        previousLabel = previousLabel.replace("length_", "length.")
        previousLabel = previousLabel.replace("angle_", "angle.")

        // Previous label to list
        let previousList = previousLabel.split(".")

        // First element formatting
        //const iconColor = EaStyle.Colors.themeForegroundMinor
        const iconColor = EaStyle.Colors.isDarkTheme ? Qt.darker(EaStyle.Colors.themeForegroundMinor, 1.2) : Qt.lighter(EaStyle.Colors.themeForegroundMinor, 1.2)
        if (list[0] === previousList[0]) {
            if (ExGlobals.Variables.iconifiedNames) {
                list[0] = `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">${list[0]}</font>`
                list[0] = list[0].replace("Phases", "gem").replace("Instrument", "microscope")
            } else {
                list[0] = `<font color=${EaStyle.Colors.themeForegroundMinor}>${list[0]}</font>`
            }
        } else {
            if (ExGlobals.Variables.iconifiedNames) {
                list[0] = `<font face="${EaStyle.Fonts.iconsFamily}">${list[0]}</font>`
                list[0] = list[0].replace("Phases", "gem").replace("Instrument", "microscope")
            } else {
                list[0] = `<font color=${EaStyle.Colors.themeForeground}>${list[0]}</font>`
            }
        }

        // Intermediate elements formatting (excluding first and last)
        for (let i = 1; i < last; ++i) {
            if (list[i] === previousList[i]) {
                list[i] = `<font color=${EaStyle.Colors.themeForegroundMinor}>${list[i]}</font>`
                if (ExGlobals.Variables.iconifiedNames) {
                    list[i] = list[i].replace("cell", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">cube</font>`)
                    list[i] = list[i].replace("length", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">ruler</font>`)
                    list[i] = list[i].replace("angle", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">less-than</font>`)
                    list[i] = list[i].replace("atoms", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">atom</font>`)
                    list[i] = list[i].replace("adp", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">arrows-alt</font>`)
                    list[i] = list[i].replace("fract", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">map-marker-alt</font>`)
                }
            } else {
                list[i] = `${list[i]}`
                if (ExGlobals.Variables.iconifiedNames) {
                    list[i] = list[i].replace("cell", `<font face="${EaStyle.Fonts.iconsFamily}">cube</font>`)
                    list[i] = list[i].replace("length", `<font face="${EaStyle.Fonts.iconsFamily}">ruler</font>`)
                    list[i] = list[i].replace("angle", `<font face="${EaStyle.Fonts.iconsFamily}">less-than</font>`)
                    list[i] = list[i].replace("atoms", `<font face="${EaStyle.Fonts.iconsFamily}">atom</font>`)
                    list[i] = list[i].replace("adp", `<font face="${EaStyle.Fonts.iconsFamily}">arrows-alt</font>`)
                    list[i] = list[i].replace("fract", `<font face="${EaStyle.Fonts.iconsFamily}">map-marker-alt</font>`)
                }
            }
        }

        // Last element formatting
        //list[last] = `<font color=${EaStyle.Colors.themeForegroundHovered}>${list[last]}</font>`
        list[last] = `${list[last]}`
        list[last] = list[last].replace("u_resolution", "resolution_u")
        list[last] = list[last].replace("v_resolution", "resolution_v")
        list[last] = list[last].replace("w_resolution", "resolution_w")
        list[last] = list[last].replace("x_resolution", "resolution_x")
        list[last] = list[last].replace("y_resolution", "resolution_y")

        // Back to string
        if (ExGlobals.Variables.iconifiedNames) {
            label = list.join(`&nbsp;&nbsp;`)
        } else {
            label = list.join(`<font color=${EaStyle.Colors.themeForegroundMinor}>.</font>`)
            label = label.replace("fract<font color=#aaaaaa>.", "fract_").replace("<font color=#aaaaaa>fract</font><font color=#aaaaaa>.", "fract_")
            label = label.replace("cell<font color=#aaaaaa>.", "cell_").replace("<font color=#aaaaaa>cell</font><font color=#aaaaaa>.", "cell_")
            label = label.replace("length<font color=#aaaaaa>.", "length_").replace("<font color=#aaaaaa>length</font><font color=#aaaaaa>.", "length_")
            label = label.replace("angle<font color=#aaaaaa>.", "angle_").replace("<font color=#aaaaaa>angle</font><font color=#aaaaaa>.", "angle_")
        }

        return label
    }

}

