<Path>Components > Tabs > Tabs with icons</Path>

Icons for the tab component can be set programmatically or declaratively. You can change the position of the icons using the ThemeVariant.

tabs-icons.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <checkbox id="iconControlCheckbox" label="Icon on top"/>
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

import com.vaadin.flow.component.AbstractField;
import com.vaadin.flow.component.tabs.Tab;
import com.vaadin.flow.component.tabs.TabVariant;
import com.vaadin.flow.component.tabs.Tabs;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.view.*;

@ViewController("tabs-icons")
@ViewDescriptor("tabs-icons.xml")
public class TabsIconsSample extends StandardView {

    @ViewComponent
    protected Tabs tabs;

    @Subscribe("iconControlCheckbox")
    protected void onIconControlCheckboxValueChane(AbstractField.ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        if (event.getValue()) {
            tabs.getChildren().forEach(tab -> ((Tab) tab).addThemeVariants(TabVariant.LUMO_ICON_ON_TOP));
        } else {
            tabs.getChildren().forEach(tab -> tab.getElement().getThemeList().clear());
        }
    }
}


