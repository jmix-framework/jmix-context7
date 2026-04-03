<Path>Components > DataGrid > DataGrid with sort event</Path>

`com.vaadin.flow.data.event.SortEvent` reacts to changes in column sorting.
The sample above shows the current sort order for each column as it changes. To add custom behavior when sorting changes — such as
triggering other updates on the view — add your own logic accessing the sort order via `event.getSortOrder()`.

data-grid-sort-event.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="ordersDc"
                    class="io.jmix.uisamples.entity.Order">
            <fetchPlan extends="_local">
                <property name="customer" fetchPlan="_local"/>
            </fetchPlan>
            <loader id="ordersLoader">
                <query>
                    <![CDATA[select e from uisamples_Order e order by e.date]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <dataGrid id="dataGrid" width="100%" minHeight="20em"
                  dataContainer="ordersDc">
            <columns>
                <column property="date"/>
                <column property="customer"/>
                <column property="amount"/>
                <column property="description"/>
            </columns>
        </dataGrid>
    </layout>
</view>



DataGridSortEvent.java

package io.jmix.uisamples.view.flowui.components.datagrid.sortevent;

import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.grid.GridSortOrder;
import com.vaadin.flow.data.event.SortEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Order;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("data-grid-sort-event")
@ViewDescriptor("data-grid-sort-event.xml")
public class DataGridSortEvent extends StandardView {

    @Autowired
    private Notifications notifications;

    @Subscribe("dataGrid")
    public void onDataGridSort(final SortEvent<DataGrid<Order>, GridSortOrder<DataGrid<Order>>> event) {
        String sortDescription;

        if (event.getSortOrder().isEmpty()) {
            sortDescription = "Default";
        } else {
            GridSortOrder<DataGrid<Order>> primaryOrder =
                    event.getSortOrder().get(0);

            Grid.Column<DataGrid<Order>> column = primaryOrder.getSorted();
            String header = column.getHeaderText();
            String directionText = switch (primaryOrder.getDirection()) {
                case ASCENDING -> "Ascending";
                case DESCENDING -> "Descending";
            };
            sortDescription = (header != null ? header : "<no header>")
                    + ": " + directionText;
        }
        notifications.show(sortDescription);
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


