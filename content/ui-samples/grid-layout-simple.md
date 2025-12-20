<Path>Layouts > GridLayout > Simple GridLayout</Path>

The `gridLayout` component is used to display components in a grid. It is based on the CSS `grid` module.

Components can be added as nested elements in XML markup, or programmatically via the `gridLayout#add` method.

To customize the gap between elements and the minimum column width, you can use the `gap` and
`minColumnWidth` properties. Properties accept CSS values and variables, such as `150px`, `2em` or `var(--lumo-space-m)`.


grid-layout-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox padding="false">
            <textField id="gapField" label="msg://gapField.label" placeholder="var(--lumo-space-s)"
                       helperText="msg://gapField.helperText" value="var(--lumo-space-m)"/>
            <textField id="columnMinWidthField" label="msg://columnMinWidthField.label"
                       placeholder="19rem"
                       helperText="msg://columnMinWidthField.helperText"
                       value="18em"/>
        </hbox>
        <split width="100%" height="100%">
            <gridLayout id="gridLayout" gap="var(--lumo-space-m)" columnMinWidth="18em" width="100%" height="100%">
                <image width="100%" height="100%" resource="icons/jmix-icon.png"/>
                <image width="100%" height="100%" resource="icons/jmix-icon.png"/>
                <image width="100%" height="100%" resource="icons/jmix-icon.png"/>
                <image width="100%" height="100%" resource="icons/jmix-icon.png"/>
                <image width="100%" height="100%" resource="icons/jmix-icon.png"/>
                <image width="100%" height="100%" resource="icons/jmix-icon.png"/>
                <image width="100%" height="100%" resource="icons/jmix-icon.png"/>
                <image width="100%" height="100%" resource="icons/jmix-icon.png"/>
            </gridLayout>
            <div/>
        </split>
    </layout>
</view>




GridLayoutSimpleSample.java

package io.jmix.uisamples.view.flowui.containers.gridlayout.simple;

import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.gridlayout.GridLayout;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.view.*;

import java.util.Objects;

@ViewController("grid-layout-simple")
@ViewDescriptor("grid-layout-simple.xml")
public class GridLayoutSimpleSample extends StandardView {

    @ViewComponent
    private GridLayout<?> gridLayout;

    @Subscribe("gapField")
    public void onGapFieldValueChangeEvent(TypedValueChangeEvent<TypedTextField<String>, String> event) {
        gridLayout.setGap(Objects.requireNonNullElse(event.getValue(), "var(--lumo-space-s)"));
    }

    @Subscribe("columnMinWidthField")
    public void onColumnMinWidthFieldValueChangeEvent(TypedValueChangeEvent<TypedTextField<String>, String> event) {
        gridLayout.setColumnMinWidth(Objects.requireNonNullElse(event.getValue(), "19rem"));
    }
}


