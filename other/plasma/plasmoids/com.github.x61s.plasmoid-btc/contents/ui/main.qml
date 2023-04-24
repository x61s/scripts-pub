// main.qml
import QtQuick 2.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 2.0
import org.kde.plasma.components 3.0 as PlasmaComponents
import org.kde.plasma.plasmoid 2.0

PlasmaComponents.Button {
    //icon.name: "bitcoin128"
    id: widget
    Plasmoid.preferredRepresentation: Plasmoid.fullRepresentation
    Layout.minimumWidth: implicitWidth

    onClicked: request()
    Component.onCompleted: {
        request()
    }
    
    Timer {
        interval: 10000
        running: true
        triggeredOnStart: false
        repeat: true
        onTriggered: {
            request();
        }
    }
    
    function request() {
        widget.icon.name = "";
        widget.text = "...";
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.HEADERS_RECEIVED) {
                print('HEADERS_RECEIVED');
            } else if (xhr.readyState === XMLHttpRequest.DONE) {
            print('DONE');
            const price = JSON.parse(xhr.responseText.toString());
            print(price.data.amount);
            //widget.icon.name = "bitcoin128";
            widget.text = "$" + price.data.amount;
            }
        }
        xhr.open("GET", "https://api.coinbase.com/v2/prices/spot?currency=USD");
        xhr.send();
    }
    
    text: 'BTC'

}

// $ plasmoidviewer -a ~/projects/plasmoid/package/
