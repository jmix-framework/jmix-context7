<Path>Layouts > BoxLayout > Flex Layout</Path>

FlexLayout is a layout component that implements Flexbox. It uses the default flex-direction and doesn't have any predetermined width or height. This component can be used as a base class for more advanced layouts.

flex-layout-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="flex-layout-simple">
        <split width="100%" themeNames="splitter-spacing">
            <flexLayout alignItems="CENTER" flexDirection="COLUMN">
                <span text="Span"/>
                <textField placeholder="TextField"/>
                <button text="Button"/>
                <button text="Button"/>
            </flexLayout>
            <flexLayout alignItems="CENTER" flexDirection="ROW"
                        justifyContent="CENTER" flexWrap="WRAP"
                        classNames="flex-with-gap">
                <span text="Span"/>
                <textField placeholder="TextField"/>
                <button text="Button"/>
                <button text="Button"/>
            </flexLayout>
        </split>
    </layout>
</view>




FlexLayoutSimpleSample.java

package io.jmix.uisamples.view.flowui.containers.boxlayout.flexbox;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("flex-layout-simple")
@ViewDescriptor("flex-layout-simple.xml")
public class FlexLayoutSimpleSample extends StandardView {
}




flex-layout-simple.css


.flex-layout-simple .flex-with-gap {
    gap: var(--vaadin-gap-s)
}


