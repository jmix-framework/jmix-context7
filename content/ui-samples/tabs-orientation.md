<Path>Components > Tabs > Tabs with orientation</Path>

tabs component support two different orientations: horizontal (default) and vertical. Use the orientation attribute to change it.

tabs-orientation.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <checkbox id="orientationCheckbox" label="Vertical"/>
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




TabsOrientationSample.java

package io.jmix.uisamples.view.flowui.components.tabs.orientation;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.tabs.Tabs;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.view.*;

@ViewController("tabs-orientation")
@ViewDescriptor("tabs-orientation.xml")
public class TabsOrientationSample extends StandardView {

    @ViewComponent
    protected Tabs tabs;

    @Subscribe("orientationCheckbox")
    protected void onOrientationCheckboxValueChane(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        tabs.setOrientation(event.getValue() ? Tabs.Orientation.VERTICAL : Tabs.Orientation.HORIZONTAL);
    }
}


