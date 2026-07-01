<Path>Components > Tabs > Tabs with icons</Path>

Icons for the tab component can be set programmatically or declaratively.

tabs-icons.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <tabs id="tabs" width="100%">
            <tab id="profileTab">
                <icon icon="USER"/>
                <span text="Profile"/>
            </tab>
            <tab id="notificationsTab">
                <icon icon="BELL"/>
                <span text="Notifications"/>
            </tab>
            <tab id="settingsTab">
                <icon icon="COG"/>
                <span text="Settings"/>
            </tab>
        </tabs>
    </layout>
</view>




TabsIconsSample.java

package io.jmix.uisamples.view.flowui.components.tabs.icons;


@ViewController("tabs-icons")
@ViewDescriptor("tabs-icons.xml")
public class TabsIconsSample extends StandardView {
}


