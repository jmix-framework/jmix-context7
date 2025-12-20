<Path>Components > DataGrid > DataGrid with empty state</Path>

You can customize the empty state display for the `DataGrid` component using `emptyStateText` and
`emptyStateComponent`.

`emptyStateText` defines a simple text, `emptyStateComponent` defines the component to display. These settings
are mutually exclusive.

`emptyStateComponent` can contain either a single component or a layout. All nested components will be available to
subscriptions in the screen controller.


data-grid-empty-state.xml

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
    <layout>
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button id="unloadBtn" action="customersDataGrid.unload"/>
        </hbox>
        <dataGrid id="customersDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="customersDc">
            <actions>
                <action id="unload" icon="ERASER" text="msg://customersDataGrid.unload.text"
                        enabled="false"/>
            </actions>
            <columns>
                <column property="name"/>
                <column property="lastName"/>
                <column property="email"/>
                <column property="age"/>
                <column property="active"/>
                <column property="grade"/>
            </columns>
            <emptyStateComponent>
                <vbox padding="false" height="100%"
                      justifyContent="CENTER" alignItems="CENTER">
                    <h3 text="msg://emptyState.text"/>
                    <button id="loadBtn" text="msg://loadBtn.text" icon="REFRESH" themeNames="primary"/>
                </vbox>
            </emptyStateComponent>
        </dataGrid>
    </layout>
</view>




DataGridEmptyStateSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.emptystate;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.kit.action.Action;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;

@ViewController("data-grid-empty-state")
@ViewDescriptor("data-grid-empty-state.xml")
public class DataGridEmptyStateSample extends StandardView {

    @ViewComponent
    private CollectionContainer<Customer> customersDc;
    @ViewComponent
    private CollectionLoader<Customer> customersDl;

    @ViewComponent("customersDataGrid.unload")
    private Action unloadAction;

    @Subscribe("customersDataGrid.unload")
    public void onCustomersDataGridUnloadActionPerformed(ActionPerformedEvent event) {
        customersDc.getMutableItems().clear();
        unloadAction.setEnabled(false);
    }

    @Subscribe("loadBtn")
    public void onLoadBtnClick(ClickEvent<JmixButton> event) {
        customersDl.load();
        unloadAction.setEnabled(true);
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


