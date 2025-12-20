<Path>Components > TextArea > Data-aware TextArea</Path>

The dataContainer and property attributes are used to connect the TextArea to an entity attribute. The dataContainer contains an entity instance; property specifies an attribute to edit.

text-area-dataaware.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <instance id="orderDc"
                  class="io.jmix.uisamples.entity.Order"
                  fetchPlan="_local"/>
    </data>
    <layout>
        <textArea id="textArea" label="Order description"
                  dataContainer="orderDc" property="description"/>
        <hbox>
            <span text="Value in the container:"/>
            <span id="spanValue"/>
        </hbox>
    </layout>
</view>




TextAreaDataawareSample.java

package io.jmix.uisamples.view.flowui.components.textarea.dataaware;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.html.Span;
import io.jmix.core.Metadata;
import io.jmix.flowui.component.textarea.JmixTextArea;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Order;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("text-area-dataaware")
@ViewDescriptor("text-area-dataaware.xml")
public class TextAreaDataawareSample extends StandardView {

    @ViewComponent
    protected InstanceContainer<Order> orderDc;
    @ViewComponent
    protected Span spanValue;

    @Autowired
    protected Metadata metadata;

    @Subscribe
    protected void onInit(InitEvent event) {
        Order order = metadata.create(Order.class);
        order.setDescription("Deliver as quickly as possible.");
        orderDc.setItem(order);
    }

    @Subscribe("textArea")
    protected void onTextAreaValueChange(ComponentValueChangeEvent<JmixTextArea, String> changeEvent) {
        spanValue.setText(orderDc.getItem().getDescription());
    }
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


