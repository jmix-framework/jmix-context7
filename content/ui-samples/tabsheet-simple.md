<Path>Layouts > TabSheet > Simple TabSheet</Path>

TabSheet container is a tabbed panel. The panel shows content of one tab at a time. The tabSheet component should contain nested tab elements describing tabs. Each tab should have only one nested element.

tabsheet-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <tabSheet width="100%">
            <tab id="tab1" label="Tab 1">
                <vbox>
                    <span text="Span 1"/>
                    <textField label="TextField 1"/>
                    <button text="Button 1"/>
                </vbox>
            </tab>
            <tab id="tab2" label="Tab 2">
                <vbox>
                    <span text="Span 2"/>
                    <textField label="TextField 2"/>
                    <button text="Button 2"/>
                </vbox>
            </tab>
        </tabSheet>
    </layout>
</view>




TabSheetSimpleSample.java

package io.jmix.uisamples.view.flowui.containers.tabsheet.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("tabsheet-simple")
@ViewDescriptor("tabsheet-simple.xml")
public class TabSheetSimpleSample extends StandardView {
}


