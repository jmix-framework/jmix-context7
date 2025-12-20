<Path>Components > Tabs > Tabs with states</Path>

A tab can be selected, unselected, or disabled. To listen for the selection event of the corresponding tab use Tabs.SelectedChangeEvent.

tabs-states.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <tabs id="tabs" width="100%">
            <tab id="tab1" label="Selected"/>
            <tab id="tab2" label="Unselected"/>
            <tab id="tab3" label="Disabled" enabled="false"/>
        </tabs>
    </layout>
</view>




TabsStatesSample.java

package io.jmix.uisamples.view.flowui.components.tabs.states;

import com.vaadin.flow.component.tabs.Tabs;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("tabs-states")
@ViewDescriptor("tabs-states.xml")
public class TabsStatesSample extends StandardView {

    @Subscribe("tabs")
    protected void onTabsSelectChangeEvent(Tabs.SelectedChangeEvent event) {
        event.getPreviousTab().setLabel("Unselected");
        event.getSelectedTab().setLabel("Selected");
    }
}


