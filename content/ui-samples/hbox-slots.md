<Path>Layouts > BoxLayout > Horizontal Layout > Horizontal Layout with items alignment</Path>

It is possible to align components inside `hbox` using special slots.

There are tree positions in total:

- `Start`
- `Middle`
- `End`

You can add an arbitrary number of components to each of these positions. To do this, you can use the corresponding
methods of `HorizontalLayout` component, or XML markup.


hbox-slots.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox width="100%">
            <startSlot>
                <span text="Span"/>
            </startSlot>
            <middleSlot>
                <textField placeholder="TextField"/>
                <button text="Button"/>
            </middleSlot>
            <endSlot>
                <button text="Button"/>
            </endSlot>
        </hbox>
    </layout>
</view>




HBoxSlotsSample.java

package io.jmix.uisamples.view.flowui.containers.boxlayout.hbox.slots;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("hbox-slots")
@ViewDescriptor("hbox-slots.xml")
public class HBoxSlotsSample extends StandardView {
}


