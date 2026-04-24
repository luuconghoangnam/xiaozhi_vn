def update_qml():
    with open('D:/xiaozhi_vn/py-xiaozhi/src/display/gui_display.qml', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = -1
    end_idx = -1
    for i, line in enumerate(lines):
        if 'property string currentEmotion:' in line:
            start_idx = i
        if 'Component.onCompleted: currentEmotionChanged()' in line:
            end_idx = i
            break

    if start_idx != -1 and end_idx != -1:
        new_lines = """                        property string currentEmotion: displayModel ? displayModel.emotionName : "neutral"

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

                        // Idle look around timer
                        Timer {
                            id: lookTimer
                            interval: 2000
                            running: true
                            repeat: true
                            onTriggered: {
                                if (avatarEyes.currentEmotion === "neutral" || avatarEyes.currentEmotion === "thinking" || avatarEyes.currentEmotion === "happy") {
                                    if (Math.random() > 0.4) {
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
                            } else { // neutral or default
                                leftBaseH = 80; leftBaseW = 60; leftBaseY = 20; leftBaseX = 40; leftBaseR = 0
                                rightBaseH = 80; rightBaseW = 60; rightBaseY = 20; rightBaseX = 140; rightBaseR = 0
                            }
                            
                            lookOffsetX = 0
                            lookOffsetY = 0
                        }
                        Component.onCompleted: currentEmotionChanged()
"""
        lines = lines[:start_idx] + [new_lines + '\n'] + lines[end_idx+1:]
        with open('D:/xiaozhi_vn/py-xiaozhi/src/display/gui_display.qml', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("Successfully updated QML file.")
    else:
        print("Could not find start or end index.")

if __name__ == "__main__":
    update_qml()
