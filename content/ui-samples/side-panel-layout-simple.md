<Path>Layouts > SidePanelLayout > Simple SidePanelLayout</Path>

`SidePanelLayout` combines the main content area with a collapsible side panel, which is useful for
details, filters, or contextual actions.

The XML presentation of the component requires two root elements:

- Main content area – first element.
- Side panel content - second element.

There is a `SidePanelLayoutCloser` helper component that closes the side panel. It can be styled to suit
your purposes or replaced by a custom button with click listener.



side-panel-layout-simple.xml

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
    </facets>
    <layout>
        <hbox alignItems="CENTER">
            <button id="toggleSidePanelButton" text="msg://toggleSidePanelButton.text"/>
            <select id="positionSelect"/>
            <checkbox id="overlayCheckbox" label="msg://overlayCheckbox.label" value="true"/>
            <checkbox id="modalCheckbox" label="msg://modalCheckbox.label" value="true"/>
        </hbox>
        <sidePanelLayout id="sidePanelLayout" height="100%" width="100%" sidePanelVerticalMinSize="15em">
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
                    <sidePanelLayoutCloser/>
                </hbox>
                <scroller scrollBarsDirection="VERTICAL" width="100%">
                    <formLayout autoResponsive="true" width="100%" expandFields="true" expandColumns="true">
                        <formRow>
                            <textField id="firstNameField" readOnly="true" datatype="string"/>
                            <textField id="lastNameField" readOnly="true" datatype="string"/>
                        </formRow>
                        <formRow>
                            <textField id="emailField" readOnly="true" colspan="2" datatype="string"/>
                        </formRow>
                    </formLayout>
                </scroller>
                <button id="sendEmailButton" text="msg://sendEmailButton.text"/>
            </vbox>
        </sidePanelLayout>
    </layout>
</view>



SidePanelLayoutSimpleSample.java

package io.jmix.uisamples.view.flowui.containers.sidepanellayout.simple;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.component.select.JmixSelect;
import io.jmix.flowui.component.sidepanellayout.SidePanelLayout;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.kit.component.sidepanellayout.SidePanelPosition;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;

@ViewController("side-panel-layout-simple")
@ViewDescriptor("side-panel-layout-simple.xml")
public class SidePanelLayoutSimpleSample extends StandardView {

    @ViewComponent
    private JmixSelect<SidePanelPosition> positionSelect;
    @ViewComponent
    private SidePanelLayout sidePanelLayout;
    @ViewComponent
    private TypedTextField<String> emailField;
    @ViewComponent
    private TypedTextField<String> lastNameField;
    @ViewComponent
    private TypedTextField<String> firstNameField;

    @Subscribe
    public void onInit(InitEvent event) {
        positionSelect.setItems(SidePanelPosition.values());
        positionSelect.setValue(sidePanelLayout.getSidePanelPosition());
        positionSelect.addValueChangeListener(e -> sidePanelLayout.setSidePanelPosition(e.getValue()));
        positionSelect.setItemLabelGenerator(Enum::name);
    }

    @Subscribe(id = "toggleSidePanelButton", subject = "clickListener")
    public void onToggleSidePanelButtonClick(ClickEvent<JmixButton> event) {
        sidePanelLayout.toggleSidePanel();
    }

    @Subscribe("overlayCheckbox")
    public void onOverlayCheckboxComponentValueChange(final ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        sidePanelLayout.setSidePanelOverlay(event.getValue());
    }

    @Subscribe("modalCheckbox")
    public void onModalCheckboxComponentValueChange(final ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        sidePanelLayout.setModal(event.getValue());
    }

    @Subscribe(id = "customersDc", target = Target.DATA_CONTAINER)
    public void onCustomersDcItemChange(final InstanceContainer.ItemChangeEvent<Customer> event) {
        emailField.setTypedValue(event.getItem() == null ? null : event.getItem().getEmail());
        lastNameField.setTypedValue(event.getItem() == null ? null : event.getItem().getLastName());
        firstNameField.setTypedValue(event.getItem() == null ? null : event.getItem().getName());
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
import org.springframework.lang.Nullable;

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


