<Path>Components > PropertyFilter > PropertyFilter with date interval operation</Path>

PropertyFilter has the DATE_INTERVAL operation. For this operation, the application uses the ValuePicker component with the custom action. It enables to open dialog to configure the date interval.

property-filter-date-interval-operation.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="ordersDc"
                    class="io.jmix.uisamples.entity.Order"
                    fetchPlan="_local">
            <loader id="ordersDl">
                <query>
                    <![CDATA[select e from uisamples_Order e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <propertyFilter property="date"
                        operation="IN_INTERVAL"
                        dataLoader="ordersDl"/>
        <dataGrid id="orderDataGrid"
                  dataContainer="ordersDc"
                  width="100%"
                  minHeight="20em">
            <columns>
                <column property="date"/>
                <column property="customer"/>
                <column property="amount"/>
                <column property="description"/>
            </columns>
        </dataGrid>
    </layout>
</view>




PropertyFilterDateIntervalOperationSample.java

package io.jmix.uisamples.view.flowui.components.propertyfilter.dateinterval;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("property-filter-date-interval-operation")
@ViewDescriptor("property-filter-date-interval-operation.xml")
public class PropertyFilterDateIntervalOperationSample extends StandardView {
}




Order.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import java.util.UUID;

@Table(name = "ORDER")
@Entity(name = "uisamples_Order")
@JmixEntity
public class Order {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "CUSTOMER_ID")
    private Customer customer;

    @Temporal(TemporalType.DATE)
    @Column(name = "DATE_", nullable = false)
    @InstanceName
    private Date date;

    @Column(name = "AMOUNT")
    private BigDecimal amount;

    @Column(name = "DESCRIPTION")
    private String description;

    @OrderBy("rowNum")
    @Composition
    @OneToMany(mappedBy = "order")
    private List<OrderItem> items;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setItems(List<OrderItem> items) {
        this.items = items;
    }

    public List<OrderItem> getItems() {
        return items;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }

    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    public Customer getCustomer() {
        return customer;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public Date getDate() {
        return date;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public BigDecimal getAmount() {
        return amount;
    }
}


