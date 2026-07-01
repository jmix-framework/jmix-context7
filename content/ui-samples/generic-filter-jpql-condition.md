<Path>Components > GenericFilter > GenericFilter with JPQL condition</Path>

In this example, the configuration was created in design-time in XML, made default using default XML attribute. So it appears right after opening the screen. A user can create conditions based on JPQL expressions by selecting Create JPQL condition in the Add search condition dialog. JPQL conditions can also be defined in the screen XML (jpqlFilter). In this example, the JPQL condition allows a user to filter orders by a product contained in order lines. You can see the condition properties in the advanced filter editor available via the Edit settings menu item.

generic-filter-jpql-condition.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:c="http://jmix.io/schema/flowui/jpql-condition">
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
        <genericFilter id="genericFilter" dataLoader="ordersDl">
            <properties include=".*"/>
            <configurations>
                <configuration id="defaultConfiguration" name="Configuration with JPQL condition" default="true">
                    <jpqlFilter label="Order items contains"
                                parameterClass="io.jmix.uisamples.entity.Product">
                        <condition>
                            <c:jpql>
                                <c:join>join {E}.items i</c:join>
                                <c:where>i.product.id = ?</c:where>
                            </c:jpql>
                        </condition>
                    </jpqlFilter>
                </configuration>
            </configurations>
        </genericFilter>
        <dataGrid id="orderDataGrid"
                  dataContainer="ordersDc"
                  width="100%"
                  minHeight="20em">
            <columns>
                <column property="date"/>
                <column property="amount"/>
                <column property="description"/>
            </columns>
        </dataGrid>
    </layout>
</view>




GenericFilterJpqlConditionSample.java

package io.jmix.uisamples.view.flowui.components.genericfilter.jpql;

import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.genericfilter.GenericFilter;
import io.jmix.flowui.component.genericfilter.configuration.DesignTimeConfiguration;
import io.jmix.flowui.component.jpqlfilter.JpqlFilter;
import io.jmix.flowui.component.jpqlfilter.JpqlFilterSupport;
import io.jmix.flowui.component.propertyfilter.SingleFilterSupport;
import io.jmix.flowui.model.DataLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Product;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("generic-filter-jpql-condition")
@ViewDescriptor("generic-filter-jpql-condition.xml")
public class GenericFilterJpqlConditionSample extends StandardView {

    @ViewComponent
    protected GenericFilter genericFilter;

    @Autowired
    protected UiComponents uiComponents;
    @Autowired
    protected JpqlFilterSupport jpqlFilterSupport;
    @Autowired
    protected SingleFilterSupport singleFilterSupport;

    @Subscribe
    protected void onInit(InitEvent event) {
        initConfiguration();
    }

    protected void initConfiguration() {
        DesignTimeConfiguration javaConfiguration = genericFilter.addConfiguration("javaConfiguration",
                "Programmatically defined configuration");
        DataLoader dataLoader = genericFilter.getDataLoader();

        javaConfiguration.getRootLogicalFilterComponent().add(createProductJpqlFilter(dataLoader));
    }

    protected JpqlFilter<Product> createProductJpqlFilter(DataLoader dataLoader) {
        JpqlFilter<Product> jpqlFilter = uiComponents.create(JpqlFilter.class);

        jpqlFilter.setConditionModificationDelegated(true);
        jpqlFilter.setDataLoader(dataLoader);
        jpqlFilter.setCondition("i.product.id = ?", "join {E}.items i");
        jpqlFilter.setParameterClass(Product.class);
        jpqlFilter.setLabel("Order items contains");

        jpqlFilter.setParameterName(jpqlFilterSupport.generateParameterName(
                jpqlFilter.getId().orElse(null),
                jpqlFilter.getParameterClass().getSimpleName()));
        jpqlFilter.setValueComponent(singleFilterSupport.generateValueComponent(
                dataLoader.getContainer().getEntityMetaClass(),
                jpqlFilter.hasInExpression(),
                jpqlFilter.getParameterClass()
        ));

        return jpqlFilter;
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




Product.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Table(name = "PRODUCT")
@Entity
@JmixEntity
public class Product {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", nullable = false)
    @InstanceName
    protected String name;

    @Column(name = "PRICE", nullable = false)
    protected BigDecimal price;

    @JoinTable(name = "PRODUCT_PRODUCT_TAG_LINK",
            joinColumns = @JoinColumn(name = "PRODUCT_ID"),
            inverseJoinColumns = @JoinColumn(name = "PRODUCT_TAG_ID"))
    @ManyToMany
    private List<ProductTag> tags;

    public Product() {
        this.id = UUID.randomUUID();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public List<ProductTag> getTags() {
        return tags;
    }

    public void setTags(List<ProductTag> tags) {
        this.tags = tags;
    }
}


