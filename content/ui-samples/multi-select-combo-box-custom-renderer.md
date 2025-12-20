<Path>Components > MultiSelectComboBox > MultiSelectComboBox with custom renderer</Path>

It is possible to customize the render of elements. You can use the setRenderer() method or @Supply annotation for it.

multi-select-combo-box-custom-renderer.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <multiSelectComboBox id="iconsMultiSelectComboBox" clearButtonVisible="true"
                  label="Icons"
                  width="20em"/>
    </layout>
</view>




MultiSelectComboBoxCustomRendererSample.java

package io.jmix.uisamples.view.flowui.components.multiselectcombobox.customrenderer;

import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.data.renderer.ComponentRenderer;
import com.vaadin.flow.data.renderer.Renderer;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.multiselectcombobox.JmixMultiSelectComboBox;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("multi-select-combo-box-custom-renderer")
@ViewDescriptor("multi-select-combo-box-custom-renderer.xml")
public class MultiSelectComboBoxCustomRendererSample extends StandardView {

    @ViewComponent
    protected JmixMultiSelectComboBox<VaadinIcon> iconsMultiSelectComboBox;

    @Autowired
    protected UiComponents uiComponents;

    @Subscribe
    protected void onInit(InitEvent event) {
        iconsMultiSelectComboBox.setItems(VaadinIcon.values());
    }

    @Supply(to = "iconsMultiSelectComboBox", subject = "renderer")
    protected Renderer<VaadinIcon> multiSelectComboBoxComponentRenderer() {
        return new ComponentRenderer<>(vaadinIcon -> {
            HorizontalLayout contentBox = uiComponents.create(HorizontalLayout.class);
            contentBox.setPadding(false);

            contentBox.add(vaadinIcon.create());
            contentBox.add(vaadinIcon.name());

            return contentBox;
        });
    }
}


