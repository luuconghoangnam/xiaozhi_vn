import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15

Rectangle {
    id: root
    color: "#121212" // Black background
    
    property bool showLogs: false

    signal manualButtonPressed()
    signal manualButtonReleased()
    signal autoButtonClicked()
    signal abortButtonClicked()
    signal modeButtonClicked()
    signal sendButtonClicked(string text)
    signal settingsButtonClicked()
    signal titleMinimize()
    signal titleClose()
    signal titleDragStart(real mouseX, real mouseY)
    signal titleDragMoveTo(real mouseX, real mouseY)
    signal titleDragEnd()

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 0
        spacing: 0

        Rectangle {
            id: titleBar
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            color: "#000000" // Pure black

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton
                onPressed: root.titleDragStart(mouse.x, mouse.y)
                onPositionChanged: if (pressed) root.titleDragMoveTo(mouse.x, mouse.y)
                onReleased: root.titleDragEnd()
            }

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 12
                anchors.rightMargin: 8
                spacing: 8

                Text {
                    text: "COONIE AI"
                    font.family: "Segoe UI"
                    font.pixelSize: 14
                    font.bold: true
                    color: "#D32F2F" // Red brand color
                }

                Item { Layout.fillWidth: true }

                Rectangle {
                    id: btnMin
                    width: 26; height: 26; radius: 0
                    color: btnMinMouse.pressed ? "#333333" : (btnMinMouse.containsMouse ? "#222222" : "transparent")
                    Text { anchors.centerIn: parent; text: "-"; font.pixelSize: 14; color: "#ffffff" }
                    MouseArea { id: btnMinMouse; anchors.fill: parent; hoverEnabled: true; onClicked: root.titleMinimize() }
                }

                Rectangle {
                    id: btnClose
                    width: 26; height: 26; radius: 0
                    color: btnCloseMouse.pressed ? "#B71C1C" : (btnCloseMouse.containsMouse ? "#D32F2F" : "transparent")
                    Text { anchors.centerIn: parent; text: "×"; font.pixelSize: 14; color: "#ffffff" }
                    MouseArea { id: btnCloseMouse; anchors.fill: parent; hoverEnabled: true; onClicked: root.titleClose() }
                }
            }
        }

        Rectangle {
            id: statusCard
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 12

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    color: "#1a1a1a"
                    border.color: "#333333"
                    border.width: 1
                    radius: 0
                    Text {
                        anchors.centerIn: parent
                        text: displayModel ? displayModel.statusText : "Trạng thái: Chưa kết nối"
                        font.family: "Consolas"
                        font.pixelSize: 14
                        font.weight: Font.Bold
                        color: "#E53935"
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredHeight: 180
                    Layout.minimumHeight: 120

                    // Minimalist Avatar Eyes (Wall-E / Cozmo style)
                    Item {
                        id: avatarEyes
                        anchors.centerIn: parent
                        width: 240
                        height: 120
                        visible: !root.showLogs

                        property string currentEmotion: displayModel ? displayModel.emotionName : "neutral"

                        // Base properties set by emotion with smooth transitions
                        property real leftBaseX: 40; Behavior on leftBaseX { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
                        property real leftBaseY: 20; Behavior on leftBaseY { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
                        property real leftBaseW: 60; Behavior on leftBaseW { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
                        property real leftBaseH: 80; Behavior on leftBaseH { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
                        property real leftBaseR: 0;  Behavior on leftBaseR { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
                        
                        property real rightBaseX: 140; Behavior on rightBaseX { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
                        property real rightBaseY: 20; Behavior on rightBaseY { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
                        property real rightBaseW: 60; Behavior on rightBaseW { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
                        property real rightBaseH: 80; Behavior on rightBaseH { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
                        property real rightBaseR: 0;  Behavior on rightBaseR { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
                        
                        // Dynamic animation properties
                        property real lookOffsetX: 0; Behavior on lookOffsetX { NumberAnimation { duration: 500; easing.type: Easing.OutSine } }
                        property real lookOffsetY: 0; Behavior on lookOffsetY { NumberAnimation { duration: 500; easing.type: Easing.OutSine } }
                        property real breatheOffsetY: 0
                        property real blinkScale: 1.0
                        property bool isBlushing: currentEmotion === "happy" || currentEmotion === "love" || currentEmotion === "laughing"

                        // Idle look around timer
                        Timer {
                            id: lookTimer
                            interval: 2000
                            running: true
                            repeat: true
                            onTriggered: {
                                if (avatarEyes.currentEmotion === "neutral" || avatarEyes.currentEmotion === "thinking" || avatarEyes.currentEmotion === "happy" || avatarEyes.currentEmotion === "love") {
                                    let rand = Math.random()
                                    if (rand > 0.7) { // Look far
                                        avatarEyes.lookOffsetX = (Math.random() - 0.5) * 60
                                        avatarEyes.lookOffsetY = (Math.random() - 0.5) * 30
                                    } else if (rand > 0.3) { // Look slightly
                                        avatarEyes.lookOffsetX = (Math.random() - 0.5) * 30
                                        avatarEyes.lookOffsetY = (Math.random() - 0.5) * 20
                                    } else {
                                        avatarEyes.lookOffsetX = 0
                                        avatarEyes.lookOffsetY = 0
                                    }
                                } else {
                                    avatarEyes.lookOffsetX = 0
                                    avatarEyes.lookOffsetY = 0
                                }
                                interval = 1500 + Math.random() * 3000
                            }
                        }

                        // Blink timer
                        Timer {
                            id: blinkTimer
                            interval: 4000
                            running: true
                            repeat: true
                            onTriggered: {
                                if (Math.random() > 0.8) {
                                    doubleBlinkAnim.start()
                                } else {
                                    blinkAnim.start()
                                }
                                interval = 2000 + Math.random() * 5000
                            }
                        }

                        // Breathe animation (continuous slight up/down movement)
                        SequentialAnimation {
                            running: true
                            loops: Animation.Infinite
                            NumberAnimation { target: avatarEyes; property: "breatheOffsetY"; to: 4; duration: 2000; easing.type: Easing.InOutSine }
                            NumberAnimation { target: avatarEyes; property: "breatheOffsetY"; to: 0; duration: 2000; easing.type: Easing.InOutSine }
                        }

                        SequentialAnimation {
                            id: blinkAnim
                            NumberAnimation { target: avatarEyes; property: "blinkScale"; to: 0.1; duration: 80; easing.type: Easing.InQuad }
                            NumberAnimation { target: avatarEyes; property: "blinkScale"; to: 1.0; duration: 100; easing.type: Easing.OutQuad }
                        }

                        SequentialAnimation {
                            id: doubleBlinkAnim
                            NumberAnimation { target: avatarEyes; property: "blinkScale"; to: 0.1; duration: 80; easing.type: Easing.InQuad }
                            NumberAnimation { target: avatarEyes; property: "blinkScale"; to: 1.0; duration: 80; easing.type: Easing.OutQuad }
                            NumberAnimation { target: avatarEyes; property: "blinkScale"; to: 0.1; duration: 80; easing.type: Easing.InQuad }
                            NumberAnimation { target: avatarEyes; property: "blinkScale"; to: 1.0; duration: 100; easing.type: Easing.OutQuad }
                        }

                        Rectangle {
                            id: leftEye
                            color: "white"
                            radius: width / 2
                            x: parent.leftBaseX + parent.lookOffsetX
                            y: parent.leftBaseY + parent.lookOffsetY + parent.breatheOffsetY + (parent.leftBaseH * (1 - parent.blinkScale) / 2)
                            width: parent.leftBaseW
                            height: parent.leftBaseH * parent.blinkScale
                            rotation: parent.leftBaseR
                        }
                        
                        Rectangle {
                            id: rightEye
                            color: "white"
                            radius: width / 2
                            x: parent.rightBaseX + parent.lookOffsetX
                            y: parent.rightBaseY + parent.lookOffsetY + parent.breatheOffsetY + (parent.rightBaseH * (1 - parent.blinkScale) / 2)
                            width: parent.rightBaseW
                            height: parent.rightBaseH * parent.blinkScale
                            rotation: parent.rightBaseR
                        }

                        // Blushing / Cheeks
                        Rectangle {
                            id: leftCheek
                            width: 30; height: 15
                            color: "#FF80AB"
                            opacity: avatarEyes.isBlushing ? 0.6 : 0.0
                            radius: 10
                            x: 45 + avatarEyes.lookOffsetX * 0.5
                            y: 110 + avatarEyes.breatheOffsetY
                            Behavior on opacity { NumberAnimation { duration: 500 } }
                        }
                        
                        Rectangle {
                            id: rightCheek
                            width: 30; height: 15
                            color: "#FF80AB"
                            opacity: avatarEyes.isBlushing ? 0.6 : 0.0
                            radius: 10
                            x: 165 + avatarEyes.lookOffsetX * 0.5
                            y: 110 + avatarEyes.breatheOffsetY
                            Behavior on opacity { NumberAnimation { duration: 500 } }
                        }
                        
                        onCurrentEmotionChanged: {
                            if (currentEmotion === "happy" || currentEmotion === "laughing" || currentEmotion === "funny") {
                                leftBaseH = 20; leftBaseW = 60; leftBaseY = 50; leftBaseX = 40; leftBaseR = -15
                                rightBaseH = 20; rightBaseW = 60; rightBaseY = 50; rightBaseX = 140; rightBaseR = 15
                            } else if (currentEmotion === "sad" || currentEmotion === "crying") {
                                leftBaseH = 30; leftBaseW = 60; leftBaseY = 40; leftBaseX = 40; leftBaseR = 15
                                rightBaseH = 30; rightBaseW = 60; rightBaseY = 40; rightBaseX = 140; rightBaseR = -15
                            } else if (currentEmotion === "angry") {
                                leftBaseH = 50; leftBaseW = 70; leftBaseY = 30; leftBaseX = 40; leftBaseR = 20
                                rightBaseH = 50; rightBaseW = 70; rightBaseY = 30; rightBaseX = 130; rightBaseR = -20
                            } else if (currentEmotion === "thinking" || currentEmotion === "confused") {
                                leftBaseH = 40; leftBaseW = 60; leftBaseY = 40; leftBaseX = 40; leftBaseR = 0
                                rightBaseH = 80; leftBaseW = 60; rightBaseY = 20; rightBaseX = 140; rightBaseR = 0
                            } else if (currentEmotion === "surprised" || currentEmotion === "shocked") {
                                leftBaseH = 90; leftBaseW = 80; leftBaseY = 15; leftBaseX = 30; leftBaseR = 0
                                rightBaseH = 90; rightBaseW = 80; rightBaseY = 15; rightBaseX = 130; rightBaseR = 0
                            } else if (currentEmotion === "sleepy" || currentEmotion === "relaxed") {
                                leftBaseH = 15; leftBaseW = 60; leftBaseY = 60; leftBaseX = 40; leftBaseR = 0
                                rightBaseH = 15; rightBaseW = 60; rightBaseY = 60; rightBaseX = 140; rightBaseR = 0
                            } else if (currentEmotion === "winking" || currentEmotion === "cool" || currentEmotion === "confident") {
                                leftBaseH = 80; leftBaseW = 60; leftBaseY = 20; leftBaseX = 40; leftBaseR = 0
                                rightBaseH = 15; rightBaseW = 60; rightBaseY = 50; rightBaseX = 140; rightBaseR = 0
                            } else if (currentEmotion === "love" || currentEmotion === "heart") {
                                leftBaseH = 50; leftBaseW = 60; leftBaseY = 40; leftBaseX = 40; leftBaseR = -10
                                rightBaseH = 50; rightBaseW = 60; rightBaseY = 40; rightBaseX = 140; rightBaseR = 10
                            } else { // neutral or default
                                leftBaseH = 80; leftBaseW = 60; leftBaseY = 20; leftBaseX = 40; leftBaseR = 0
                                rightBaseH = 80; rightBaseW = 60; rightBaseY = 20; rightBaseX = 140; rightBaseR = 0
                            }
                            
                            lookOffsetX = 0
                            lookOffsetY = 0
                        }
                        Component.onCompleted: currentEmotionChanged()

                    }

                    Rectangle {
                        id: logContainer
                        anchors.fill: parent
                        visible: root.showLogs
                        color: "#000000"
                        radius: 0
                        border.color: "#333333"
                        border.width: 1

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 4
                            spacing: 2

                            Text {
                                text: "SYSTEM LOGS"
                                font.family: "Consolas"
                                font.pixelSize: 10
                                font.bold: true
                                color: "#D32F2F"
                                Layout.leftMargin: 4
                            }

                            Flickable {
                                id: logFlickable
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                contentWidth: width
                                contentHeight: logTextItem.paintedHeight
                                clip: true

                                Text {
                                    id: logTextItem
                                    width: parent.width
                                    text: displayModel ? displayModel.logsText : ""
                                    font.family: "Consolas"
                                    font.pixelSize: 10
                                    color: "#ff8a80"
                                    wrapMode: Text.WordWrap
                                }
                                
                                onContentHeightChanged: {
                                    logFlickable.contentY = Math.max(0, logFlickable.contentHeight - logFlickable.height)
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    color: "transparent"
                    Text {
                        anchors.fill: parent
                        anchors.margins: 5
                        text: displayModel ? displayModel.ttsText : "Sẵn sàng"
                        font.family: "Segoe UI"
                        font.pixelSize: 14
                        color: "#ffffff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        wrapMode: Text.WordWrap
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 80
                    color: "#1a1a1a"
                    radius: 0
                    border.color: "#333333"
                    border.width: 1

                    Flickable {
                        anchors.fill: parent
                        anchors.margins: 8
                        contentWidth: width
                        contentHeight: detailTextItem.paintedHeight
                        clip: true

                        Text {
                            id: detailTextItem
                            width: parent.width
                            text: displayModel ? displayModel.detailText : "Coonie đang chờ anh gọi..."
                            font.family: "Segoe UI"
                            font.pixelSize: 12
                            color: "#cccccc"
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignTop
                            wrapMode: Text.WordWrap
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 120
            color: "#0a0a0a"

            ColumnLayout {
                anchors.fill: parent
                anchors.leftMargin: 12
                anchors.rightMargin: 12
                anchors.bottomMargin: 10
                spacing: 8

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 6

                    Button {
                        id: manualBtn
                        Layout.fillWidth: true
                        Layout.preferredHeight: 38
                        text: "Giữ để nói"
                        visible: displayModel ? !displayModel.autoMode : true
                        background: Rectangle { color: manualBtn.pressed ? "#7F0000" : (manualBtn.hovered ? "#D32F2F" : "#B71C1C"); radius: 0 }
                        contentItem: Text { text: manualBtn.text; font.family: "Segoe UI"; font.bold: true; font.pixelSize: 12; color: "white"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                        onPressed: { manualBtn.text = "Thả để dừng"; root.manualButtonPressed() }
                        onReleased: { manualBtn.text = "Giữ để nói"; root.manualButtonReleased() }
                    }

                    Button {
                        id: autoBtn
                        Layout.fillWidth: true
                        Layout.preferredHeight: 38
                        text: displayModel ? displayModel.buttonText : "Bắt đầu"
                        visible: displayModel ? displayModel.autoMode : false
                        background: Rectangle { color: autoBtn.pressed ? "#7F0000" : (autoBtn.hovered ? "#D32F2F" : "#B71C1C"); radius: 0 }
                        contentItem: Text { text: autoBtn.text; font.family: "Segoe UI"; font.bold: true; font.pixelSize: 12; color: "white"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                        onClicked: root.autoButtonClicked()
                    }

                    Button {
                        id: abortBtn
                        Layout.fillWidth: true
                        Layout.preferredHeight: 38
                        text: "Ngắt"
                        background: Rectangle { color: abortBtn.pressed ? "#1a1a1a" : (abortBtn.hovered ? "#333333" : "#222222"); radius: 0; border.color: "#B71C1C"; border.width: 1 }
                        contentItem: Text { text: abortBtn.text; font.family: "Segoe UI"; font.pixelSize: 12; color: "white"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                        onClicked: root.abortButtonClicked()
                    }

                    Button {
                        id: modeBtn
                        Layout.fillWidth: true
                        Layout.preferredHeight: 38
                        text: displayModel ? displayModel.modeText : "Thủ công"
                        background: Rectangle { color: modeBtn.pressed ? "#1a1a1a" : (modeBtn.hovered ? "#333333" : "#222222"); radius: 0; border.color: "#B71C1C"; border.width: 1 }
                        contentItem: Text { text: modeBtn.text; font.family: "Segoe UI"; font.pixelSize: 12; color: "white"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                        onClicked: root.modeButtonClicked()
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 6

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 38
                        color: "#000000"
                        radius: 0
                        border.color: textInput.activeFocus ? "#D32F2F" : "#333333"
                        border.width: 1

                        TextInput {
                            id: textInput
                            anchors.fill: parent
                            anchors.leftMargin: 10
                            anchors.rightMargin: 10
                            verticalAlignment: TextInput.AlignVCenter
                            font.family: "Segoe UI"
                            font.pixelSize: 12
                            color: "#ffffff"
                            selectByMouse: true
                            clip: true
                            Text { anchors.fill: parent; text: "Nhập văn bản..."; font: textInput.font; color: "#666666"; verticalAlignment: Text.AlignVCenter; visible: !textInput.text && !textInput.activeFocus }
                            Keys.onReturnPressed: { if (textInput.text.trim().length > 0) { root.sendButtonClicked(textInput.text); textInput.text = "" } }
                        }
                    }

                    Button {
                        id: sendBtn
                        Layout.preferredWidth: 72
                        Layout.preferredHeight: 38
                        text: "Gửi"
                        background: Rectangle { color: sendBtn.pressed ? "#7F0000" : (sendBtn.hovered ? "#D32F2F" : "#B71C1C"); radius: 0 }
                        contentItem: Text { text: sendBtn.text; font.family: "Segoe UI"; font.bold: true; font.pixelSize: 12; color: "white"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                        onClicked: { if (textInput.text.trim().length > 0) { root.sendButtonClicked(textInput.text); textInput.text = "" } }
                    }

                    Button {
                        id: toggleLogsBtn
                        Layout.preferredWidth: 60
                        Layout.preferredHeight: 38
                        text: root.showLogs ? "Avatar" : "Logs"
                        background: Rectangle { color: toggleLogsBtn.pressed ? "#1a1a1a" : (toggleLogsBtn.hovered ? "#333333" : "#222222"); radius: 0; border.color: "#B71C1C"; border.width: 1 }
                        contentItem: Text { text: toggleLogsBtn.text; font.family: "Segoe UI"; font.pixelSize: 12; color: "white"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                        onClicked: root.showLogs = !root.showLogs
                    }

                    Button {
                        id: settingsBtn
                        Layout.preferredWidth: 70
                        Layout.preferredHeight: 38
                        text: "Cài đặt"
                        background: Rectangle { color: settingsBtn.pressed ? "#1a1a1a" : (settingsBtn.hovered ? "#333333" : "#222222"); radius: 0; border.color: "#B71C1C"; border.width: 1 }
                        contentItem: Text { text: settingsBtn.text; font.family: "Segoe UI"; font.pixelSize: 12; color: "white"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                        onClicked: root.settingsButtonClicked()
                    }
                }
            }
        }
    }
}
