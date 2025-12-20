<Path>Layouts > BoxLayout > Vertical Layout</Path>

vbox is a BoxLayout container with vertical placement of components.

vbox-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <vbox>
            <span text="Span"/>
            <textField placeholder="TextField"/>
            <button text="Button"/>
            <button text="Button"/>
        </vbox>
    </layout>
</view>




VBoxSimpleSample.java

package io.jmix.uisamples.view.flowui.containers.boxlayout.vbox;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("vbox-simple")
@ViewDescriptor("vbox-simple.xml")
public class VBoxSimpleSample extends StandardView {
}


