<Path>Layouts > TabSheet > TabSheet with states</Path>

A `tab` can be selected, unselected, or disabled.

To listen for the selection event of the corresponding `tab` use `JmixTabSheet.SelectedChangeEvent`.


tabsheet-states.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <tabSheet id="tabSheet" width="100%">
            <tab id="tab1" label="Selected">
                <vbox>
                    <span text="Span 1"/>
                    <textField label="TextField 1"/>
                    <button text="Button 1"/>
                </vbox>
            </tab>
            <tab id="tab2" label="Unselected">
                <vbox>
                    <span text="Span 2"/>
                    <textField label="TextField 2"/>
                    <button text="Button 2"/>
                </vbox>
            </tab>
            <tab id="tab3" label="Disabled" enabled="false">
                <vbox>
                    <span text="Span 3"/>
                    <textField label="TextField 3"/>
                    <button text="Button 3"/>
                </vbox>
            </tab>
        </tabSheet>
    </layout>
</view>




TabSheetStatesSample.java

package io.jmix.uisamples.view.flowui.containers.tabsheet.states;

import io.jmix.flowui.component.tabsheet.JmixTabSheet;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("tabsheet-states")
@ViewDescriptor("tabsheet-states.xml")
public class TabSheetStatesSample extends StandardView {

    @Subscribe("tabSheet")
    public void onTabSheetSelectChangeEvent(JmixTabSheet.SelectedChangeEvent event) {
        event.getPreviousTab().setLabel("Unselected");
        event.getSelectedTab().setLabel("Selected");
    }
}


