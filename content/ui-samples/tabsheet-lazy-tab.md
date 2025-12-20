<Path>Layouts > TabSheet > TabSheet with lazy tabs</Path>

This example describes one way to create a lazy-loading tab. Lazy tabs do not load their content when a view is opened, which reduces the number of components in memory. Components within a tab are loaded only when user selects the tab. Additionally, if a lazy tab includes visual components linked to a data source, containing a JPQL query, this query will not be invoked as well. As a result, the view opens quicker and data is loaded only when user requests it by selecting this tab. In this example, when you open the view, you can see that the content, located inside lazy LazyTab 1, is null. When you select this tab, checkComponents() method is called again, and the components appear.

tabsheet-lazy-tab.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <tabSheet id="tabSheet" width="100%" themeNames="bordered">
            <tab id="tab1" label="Tab 1">
                <vbox>
                    <span text="Span 1"/>
                    <textField label="TextField 1"/>
                    <button text="Button 1"/>
                </vbox>
            </tab>
        </tabSheet>
        <span text="Created content:"/>
        <span id="spanInfo"/>
    </layout>
</view>




TabSheetLazyTabSample.java

package io.jmix.uisamples.view.flowui.containers.tabsheet.lazytab;

import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.tabsheet.JmixTabSheet;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.component.lazycomponent.LazyComponent;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@ViewController("tabsheet-lazy-tab")
@ViewDescriptor("tabsheet-lazy-tab.xml")
public class TabSheetLazyTabSample extends StandardView {

    @ViewComponent
    protected JmixTabSheet tabSheet;
    @ViewComponent
    protected Span spanInfo;

    @Autowired
    protected UiComponents uiComponents;

    @Subscribe
    protected void onInit(InitEvent event) {
        tabSheet.add("LazyTab 1", new LazyComponent(this::getLazyTabContent));
        tabSheet.add("LazyTab 2", new LazyComponent(this::getLazyTabContent));

        checkComponents();
        tabSheet.addSelectedChangeListener(e -> checkComponents());
    }

    protected Component getLazyTabContent() {
        VerticalLayout content = uiComponents.create(VerticalLayout.class);

        Span info = uiComponents.create(Span.class);
        info.setText("Lazy Span");

        TypedTextField<String> textField = uiComponents.create(TypedTextField.class);
        textField.setLabel("Lazy textField");

        JmixButton button = uiComponents.create(JmixButton.class);
        button.setText("Lazy button");

        content.add(info, textField, button);
        return content;
    }

    protected void checkComponents() {
        StringBuilder sb = new StringBuilder("Tab 1 = ");
        List<Component> tab1Content = tabSheet.getContentByTab(tabSheet.getTabAt(0)).getChildren().toList();
        sb.append(tab1Content.isEmpty() ? "null" : "true");

        sb.append(", LazyTab 1 = ");
        List<Component> tab2Content = tabSheet.getContentByTab(tabSheet.getTabAt(1)).getChildren().toList();
        sb.append(tab2Content.isEmpty() ? "null" : "true");

        sb.append(", LazyTab 2 = ");
        List<Component> tab3Content = tabSheet.getContentByTab(tabSheet.getTabAt(2)).getChildren().toList();
        sb.append(tab3Content.isEmpty() ? "null" : "true");

        spanInfo.setText(sb.toString());
    }
}




LazyComponent.java

package io.jmix.uisamples.component.lazycomponent;

import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.function.SerializableSupplier;

public class LazyComponent extends Div {

    public LazyComponent(SerializableSupplier<? extends Component> supplier) {
        initComponent(supplier);
    }

    protected void initComponent(SerializableSupplier<? extends Component> supplier) {
        addAttachListener(event -> {
            if (getElement().getChildCount() == 0) {
                add(supplier.get());
            }
        });
    }
}


