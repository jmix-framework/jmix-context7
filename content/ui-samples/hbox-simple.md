<Path>Layouts > BoxLayout > Horizontal Layout > Simple Horizontal Layout</Path>

hbox is a BoxLayout container with horizontal placement of components. This example also shows how to align all components in an hbox with alignItems attribute.

hbox-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox alignItems="CENTER" wrap="true">
            <span text="Span"/>
            <textField placeholder="TextField"/>
            <button text="Button"/>
            <button text="Button"/>
        </hbox>
    </layout>
</view>




HBoxSimpleSample.java

package io.jmix.uisamples.view.flowui.containers.boxlayout.hbox.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("hbox-simple")
@ViewDescriptor("hbox-simple.xml")
public class HBoxSimpleSample extends StandardView {
}


