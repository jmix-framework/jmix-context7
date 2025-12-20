<Path>Components > Image > Image with ThemeVariant</Path>

The Image component has several theme variants: contain cover fill scale-down You can set these styles to the Image component using the themeNames attribute either in the XML descriptor or in the view controller using constants from JmixImageVariant class.

image-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <select id="themeSelect" label="ThemeName"/>
        <vbox classNames="items-center justify-center bordered-panel"
              height="15em" width="20em">
            <image id="image" resource="icons/jmix-icon.png" height="10em" width="15em"
                   themeNames="contain"/>
        </vbox>
    </layout>
</view>




ImageThemeVariant.java

package io.jmix.uisamples.view.flowui.components.image.themevariant;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.dom.ThemeList;
import io.jmix.flowui.component.image.JmixImage;
import io.jmix.flowui.component.image.JmixImageVariant;
import io.jmix.flowui.component.select.JmixSelect;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.view.*;

import java.util.Arrays;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@ViewController("image-theme-variant")
@ViewDescriptor("image-theme-variant.xml")
public class ImageThemeVariant extends StandardView {

    @ViewComponent
    protected JmixSelect<JmixImageVariant> themeSelect;
    @ViewComponent
    protected JmixImage<?> image;

    @Subscribe
    protected void onInit(InitEvent event) {
        ComponentUtils.setItemsMap(themeSelect, getThemeSelectItemsMap());
        themeSelect.setValue(JmixImageVariant.CONTAIN);
    }

    @Subscribe("themeSelect")
    protected void onThemeSelectValueChange(
            ComponentValueChangeEvent<JmixSelect<JmixImageVariant>, JmixImageVariant> event) {
        ThemeList themeList = image.getElement().getThemeList();
        themeList.clear();
        themeList.add(event.getValue().getVariantName());
    }

    protected Map<JmixImageVariant, String> getThemeSelectItemsMap() {
        return Arrays.stream(JmixImageVariant.values())
                .collect(Collectors.toMap(Function.identity(), variant -> variant.name().replace('_', ' ')));
    }
}


