<Path>Components > TwinColumn > TwinColumn with ThemeVariant</Path>

The TwinColumn component has several theme variants: no-border no-spaces-between-actions You can set these styles to the TwinColumn component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TwinColumnVariant class.

twin-column-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_local">
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <hbox width="100%" wrap="true">
            <checkboxGroup id="twinColumnThemeCheckboxGroup" label="ThemeVariants" themeNames="horizontal"/>
        </hbox>
        <twinColumn id="customersTwinColumn" label="Customers TwinColumn" itemsContainer="customersDc"/>
    </layout>
</view>




TwinColumnThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.twincolumn.themevariant;

import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.component.twincolumn.TwinColumn;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.kit.component.twincolumn.TwinColumnVariant;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;

@ViewController("twin-column-theme-variant")
@ViewDescriptor("twin-column-theme-variant.xml")
public class TwinColumnThemeVariantSample extends StandardView {

    @ViewComponent
    private JmixCheckboxGroup<TwinColumnVariant> twinColumnThemeCheckboxGroup;
    @ViewComponent
    private TwinColumn<Customer> customersTwinColumn;

    @Subscribe
    public void onInit(InitEvent event) {
        ComponentUtils.setItemsMap(twinColumnThemeCheckboxGroup, getTwinColumnVariantItemsMap());
    }

    @Subscribe("twinColumnThemeCheckboxGroup")
    public void onTwinColumnThemeCheckboxGroupValueChange(
            TypedValueChangeEvent<JmixCheckboxGroup<TwinColumnVariant>, Collection<TwinColumnVariant>> event) {
        if (event.getValue() == null) {
            return;
        }

        //clear
        customersTwinColumn.getElement().getThemeList().clear();

        event.getValue().forEach(customersTwinColumn::addThemeVariants);
    }

    private Map<TwinColumnVariant, String> getTwinColumnVariantItemsMap() {
        LinkedHashMap<TwinColumnVariant, String> map = new LinkedHashMap<>();

        map.put(TwinColumnVariant.NO_BORDER, "No border");
        map.put(TwinColumnVariant.NO_SPACE_BETWEEN_ACTIONS, "No space between actions");
        return map;
    }
}


