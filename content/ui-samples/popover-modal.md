<Path>Components > Popover > Modal Popover</Path>

A modal popover works as a small dialog anchored to its target. With `modal="true"`, it blocks interaction with the rest of the UI, moves the focus inside and keeps it there until the popover closes. `backdropVisible="true"` additionally dims the UI behind it.

A click outside a modal popover closes it without triggering the component under the pointer. To keep the popover open until the user presses a button inside it, set `closeOnOutsideClick` to `false`.

The popover content belongs to the view, so it can include data-aware components. Here, property filters are bound to the loader of the grid and are not applied automatically (`autoApply="false"`), and the **Apply** button loads the data and closes the popover.


popover-modal.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_local">
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e order by e.lastName]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <hbox width="100%" justifyContent="END">
            <button id="filterButton" text="Filter" icon="FILTER"/>
        </hbox>
        <popover id="filterPopover" target="filterButton" position="BOTTOM_END" width="22em"
                 modal="true" backdropVisible="true">
            <vbox padding="false">
                <h4 text="Filter customers"/>
                <propertyFilter id="lastNameFilter" property="lastName" operation="CONTAINS"
                                dataLoader="customersDl" autoApply="false" width="100%"/>
                <propertyFilter id="ageFilter" property="age" operation="GREATER_OR_EQUAL"
                                dataLoader="customersDl" autoApply="false" width="100%"/>
                <hbox>
                    <button id="applyButton" text="Apply" themeNames="primary"/>
                    <button id="clearButton" text="Clear"/>
                </hbox>
            </vbox>
        </popover>
        <dataGrid id="customersDataGrid"
                  dataContainer="customersDc"
                  width="100%"
                  minHeight="20em">
            <columns>
                <column property="name"/>
                <column property="lastName"/>
                <column property="email"/>
                <column property="age"/>
            </columns>
        </dataGrid>
    </layout>
</view>




PopoverModalSample.java

package io.jmix.uisamples.view.flowui.components.popover.modal;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.popover.Popover;
import io.jmix.flowui.component.propertyfilter.PropertyFilter;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;

@ViewController("popover-modal")
@ViewDescriptor("popover-modal.xml")
public class PopoverModalSample extends StandardView {

    @ViewComponent
    private Popover filterPopover;
    @ViewComponent
    private PropertyFilter<String> lastNameFilter;
    @ViewComponent
    private PropertyFilter<Integer> ageFilter;
    @ViewComponent
    private CollectionLoader<Customer> customersDl;

    @Subscribe(id = "applyButton", subject = "clickListener")
    public void onApplyButtonClick(ClickEvent<JmixButton> event) {
        customersDl.load();
        filterPopover.close();
    }

    @Subscribe(id = "clearButton", subject = "clickListener")
    public void onClearButtonClick(ClickEvent<JmixButton> event) {
        lastNameFilter.clear();
        ageFilter.clear();
        customersDl.load();
        filterPopover.close();
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


