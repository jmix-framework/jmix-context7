<Path>Layouts > SidePanelLayout > SidePanelLayout with resizable panel</Path>

The side panel of `SidePanelLayout` can be resized by the user at runtime. Set the `sidePanelResizable` attribute
to `true` and drag the handle on the panel's inner edge.

The size stays within the bounds defined by the `sidePanelHorizontalMinSize` / `sidePanelHorizontalMaxSize` and
`sidePanelVerticalMinSize` / `sidePanelVerticalMaxSize` attributes.

The `resizer-small` theme renders the handle as a thin line with a grip that appears on hover.

`SidePanelAfterResizeEvent` is fired once the user releases the handle. It provides the new size in `px`.

The chosen size is saved by the `settings` facet and is restored when the view is opened again.


side-panel-layout-resizable.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
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
        <settings auto="true"/>
    </facets>
    <layout>
        <hbox alignItems="CENTER">
            <button id="toggleSidePanelButton" text="msg://toggleSidePanelButton.text"/>
            <select id="positionSelect"/>
            <checkbox id="smallResizerCheckbox" label="msg://smallResizerCheckbox.label"/>
            <button id="resetSizeButton" text="msg://resetSizeButton.text"/>
        </hbox>
        <sidePanelLayout id="sidePanelLayout" height="100%" width="100%"
                         sidePanelResizable="true"
                         sidePanelOverlay="false"
                         modal="false"
                         sidePanelHorizontalSize="25em"
                         sidePanelHorizontalMinSize="15em"
                         sidePanelHorizontalMaxSize="40em"
                         sidePanelVerticalSize="15em"
                         sidePanelVerticalMinSize="10em"
                         sidePanelVerticalMaxSize="25em">
            <dataGrid id="customersDataGrid"
                      width="100%"
                      minHeight="20em"
                      dataContainer="customersDc">
                <columns>
                    <column property="name"/>
                    <column property="lastName"/>
                    <column property="email"/>
                    <column property="age"/>
                    <column property="active"/>
                    <column property="grade"/>
                </columns>
            </dataGrid>
            <vbox id="sidePanelBox" height="100%" width="100%">
                <hbox width="100%" justifyContent="BETWEEN" alignItems="CENTER">
                    <h2 id="header" text="msg://header.text"/>
                    <sidePanelLayoutCloser themeNames="tertiary"/>
                </hbox>
                <span id="hintText" text="msg://hintText.text"/>
            </vbox>
        </sidePanelLayout>
    </layout>
</view>




SidePanelLayoutResizableSample.java

package io.jmix.uisamples.view.flowui.containers.sidepanellayout.resizable;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.component.select.JmixSelect;
import io.jmix.flowui.component.sidepanellayout.SidePanelLayout;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.kit.component.sidepanellayout.SidePanelAfterResizeEvent;
import io.jmix.flowui.kit.component.sidepanellayout.SidePanelPosition;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("side-panel-layout-resizable")
@ViewDescriptor("side-panel-layout-resizable.xml")
public class SidePanelLayoutResizableSample extends StandardView {

    private static final String DEFAULT_HORIZONTAL_SIZE = "25em";
    private static final String DEFAULT_VERTICAL_SIZE = "15em";

    @Autowired
    private Notifications notifications;
    @ViewComponent
    private MessageBundle messageBundle;

    @ViewComponent
    private JmixSelect<SidePanelPosition> positionSelect;
    @ViewComponent
    private SidePanelLayout sidePanelLayout;

    @Subscribe
    public void onInit(InitEvent event) {
        positionSelect.setItems(SidePanelPosition.values());
        positionSelect.setValue(sidePanelLayout.getSidePanelPosition());
        positionSelect.addValueChangeListener(e -> sidePanelLayout.setSidePanelPosition(e.getValue()));
        positionSelect.setItemLabelGenerator(Enum::name);

        sidePanelLayout.openSidePanel();
    }

    @Subscribe(id = "toggleSidePanelButton", subject = "clickListener")
    public void onToggleSidePanelButtonClick(ClickEvent<JmixButton> event) {
        sidePanelLayout.toggleSidePanel();
    }

    @Subscribe("smallResizerCheckbox")
    public void onSmallResizerCheckboxComponentValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        sidePanelLayout.setThemeName("resizer-small", event.getValue());
    }

    @Subscribe(id = "resetSizeButton", subject = "clickListener")
    public void onResetSizeButtonClick(ClickEvent<JmixButton> event) {
        sidePanelLayout.setSidePanelHorizontalSize(DEFAULT_HORIZONTAL_SIZE);
        sidePanelLayout.setSidePanelVerticalSize(DEFAULT_VERTICAL_SIZE);
    }

    @Subscribe(id = "sidePanelLayout", subject = "addSidePanelAfterResizeListener")
    public void onSidePanelLayoutAfterResize(SidePanelAfterResizeEvent event) {
        notifications.show(messageBundle.formatMessage("sidePanelResized.notification", event.getSize()));
    }
}




Customer.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import org.jspecify.annotations.Nullable;

import java.util.UUID;

@Table(name = "CUSTOMER")
@Entity
@JmixEntity
public class Customer {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", length = 50, nullable = false)
    protected String name;

    @Column(name = "LAST_NAME", length = 100, nullable = false)
    protected String lastName;

    @Email
    @Column(name = "EMAIL", nullable = false)
    protected String email;

    @Column(name = "AGE")
    protected Integer age;

    @Column(name = "ACTIVE", nullable = false)
    protected Boolean active = false;

    @Column(name = "GRADE")
    protected Integer grade;

    public Boolean getActive() {
        return active;
    }

    public Customer() {
        this.id = UUID.randomUUID();
    }

    @InstanceName
    @DependsOnProperties({"name", "lastName"})
    public String getInstanceName() {
        return name + " " + lastName;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setGrade(@Nullable CustomerGrade grade) {
        this.grade = grade == null ? null : grade.getId();
    }

    @Nullable
    public CustomerGrade getGrade() {
        return grade == null ? null : CustomerGrade.fromId(grade);
    }

    public void setActive(Boolean active) {
        this.active = active;
    }

    public Boolean isActive() {
        return active;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Integer getAge() {
        return age;
    }
}


