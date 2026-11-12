---
title: firestore
category: GCP
description: 'GCP note: Firestore.'
tags:
- gcp
- databases
---


# firestore

## Firestore
**Serverless, NoSQL document database** for mobile, web, and server applications

**AWS Equivalent:** DynamoDB

### Firestore Modes

| Attribute | Native mode (Recommended) | Datastore mode |
|---|---|---|
| Consistency | **Strongly consistent** | Eventual consistency option |
| Real-time updates | **Real-time updates** with listeners | No real-time updates |
| Offline support | **Offline support** for mobile/web | - |
| Querying | Rich querying capabilities | - |
| Backend and API | - | Firestore backend with Datastore API |
| Clients | - | Server-side applications only |
| Switching | **Cannot switch to Datastore mode** | **Cannot switch to Native mode** |
| Use for | Mobile apps, web apps, real-time applications | Existing Datastore apps, server workloads without real-time needs |

**This document focuses on Native Mode** as it's recommended for new applications.

### Key Features
- **Fully managed and serverless** (no servers to provision)
- **Automatic scaling** (0 to millions of concurrent users)
- **Strong consistency** by default
- **Real-time synchronization** across clients
- **Offline mode** with local cache
- **ACID transactions**
- **Built-in security rules**
- **Multi-region replication**
- **Pay per operation** (no minimum cost)

### Firestore vs DynamoDB

| Feature | Firestore | DynamoDB |
|---------|-----------|----------|
| Data Model | Document (JSON-like) | Key-value, Document |
| Consistency | Strong | Strong (eventually for global) |
| Real-time | Yes (listeners) | No (use streams) |
| Offline Support | Native | Via AppSync |
| Querying | Rich queries, compound | Limited, requires GSI |
| Pricing | Per operation + storage | Per RCU/WCU or on-demand |
| Minimum Cost | $0 (free tier) | $0 (pay per request) |
| Transactions | ACID, up to 500 docs | ACID, up to 100 items |

### Data Model
#### Structure Hierarchy
```text
Database (Project)
  └── Collection (users)
      └── Document (user123)
          ├── Fields (name, email, age)
          └── Sub-collection (orders)
              └── Document (order456)
                  └── Fields (total, items)
```

#### Documents
- JSON-like structure with fields
- Maximum 1 MB per document
- Support nested objects (maps) up to 100 levels
- Can contain sub-collections
- Automatically indexed by default

#### Collections
- Container for documents
- No schema enforcement (documents can have different fields)
- Created implicitly when first document added
- Cannot contain other collections directly (only via documents)

#### Supported Data Types
- String, Number, Boolean, Map, Array
- Null, Timestamp, GeoPoint, Reference
- Bytes (up to 1 MB)

### Querying
#### Basic Queries
```javascript
// Get single document
const doc = await db.collection('users').doc('user123').get();

// Query collection
const query = db.collection('users')
  .where('age', '>', 18)
  .where('city', '==', 'NYC')
  .orderBy('age')
  .limit(10);

const snapshot = await query.get();
```

#### Compound Queries
- **Multiple equality filters** (no index needed)
- **One range filter** (<, <=, >, >=) per query
- **Requires composite index** for complex queries
- Automatic index creation suggestions in console

#### Query Limitations
- Cannot query across collections (only within one collection or collection group)
- **OR queries** supported (in() operator with up to 30 values)
- **NOT-EQUAL queries** supported
- Inequality filters on single field only
- No full-text search (use Algolia or [[bigquery|BigQuery]])

### Indexing
#### Automatic Indexing
- Single-field ascending/descending indexes created automatically
- Supports basic queries out of the box

#### Composite Indexes
- **Required for queries with multiple fields**
- Created manually or automatically (console suggests)
- Can specify via Firebase CLI or console
- Built asynchronously (can take time for large collections)

```javascript
// This query requires a composite index
db.collection('products')
  .where('category', '==', 'electronics')
  .where('price', '<', 500)
  .orderBy('price')
  .orderBy('rating', 'desc');
```

#### Index Exemptions
- Can disable automatic indexing for specific fields
- Reduces index storage costs
- Use for fields never queried

### Real-Time Listeners
```javascript
// Listen to document changes
db.collection('users').doc('user123')
  .onSnapshot((doc) => {
    console.log("Current data: ", doc.data());
  });

// Listen to query results
db.collection('messages')
  .where('roomId', '==', 'room1')
  .orderBy('timestamp')
  .onSnapshot((snapshot) => {
    snapshot.docChanges().forEach((change) => {
      if (change.type === 'added') console.log('New: ', change.doc.data());
      if (change.type === 'modified') console.log('Modified: ', change.doc.data());
      if (change.type === 'removed') console.log('Removed: ', change.doc.data());
    });
  });
```

### Offline Support
- **Automatic local caching** for mobile/web SDKs
- Writes queued locally when offline
- **Automatic synchronization** when back online
- Conflict resolution (last write wins by default)
- Manual cache configuration available

### Transactions
- **ACID guarantees**
- **Up to 500 documents** per transaction
- Read operations must come before writes
- Automatic retry on contention
- 10-second timeout

```javascript
const transaction = db.runTransaction(async (t) => {
  const doc = await t.get(docRef);
  const newValue = doc.data().value + 1;
  t.update(docRef, { value: newValue });
});
```

### Batch Writes
- **Up to 500 operations** per batch
- Atomic (all succeed or all fail)
- **No reads allowed** in batch
- More efficient than individual writes

```javascript
const batch = db.batch();
batch.set(docRef1, { name: 'Alice' });
batch.update(docRef2, { age: 30 });
batch.delete(docRef3);
await batch.commit();
```

### Security Rules
**AWS Equivalent:** IAM policies + AppSync resolvers
- **Declarative rules language**
- Control read/write access per document
- Validate data structure
- **Deployed independently** from application code

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow authenticated users to read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }

    // Validate data structure
    match /posts/{postId} {
      allow create: if request.resource.data.title is string
                    && request.resource.data.title.size() > 0
                    && request.resource.data.title.size() <= 100;
    }
  }
}
```

### Database Locations

| Type | Examples | SLA | Cost | Notes |
|---|---|---|---|---|
| Multi-Region | `nam5`: us-central, us-east (**lowest latency in US**); `eur3`: europe-west1, europe-west4 | 99.99% | Higher than regional | **Data replicated across regions** |
| Regional | Single region (e.g., us-east1, europe-west2) | 99.9% | Lower | Use when data residency required |

**Location cannot be changed after creation**

### Pricing

| Operation | Price |
|---|---|
| Document read | $0.036 per 100,000 reads |
| Query (even if no results) | Counted as 1 read |
| Document write, update, delete | $0.108 per 100,000 writes |
| Document delete | $0.012 per 100,000 deletes |
| Storage (multi-region) | $0.108 per GB/month |
| Storage (regional) | $0.018 per GB/month |
| Network egress | 10 GB/month free, additional egress charged |

**Free Tier (Spark Plan):**
- 50,000 reads/day
- 20,000 writes/day
- 20,000 deletes/day
- 1 GB storage
- **Ideal for small apps and prototypes**

**Example cost:**
- 1M reads/month + 500K writes/month + 1 GB storage ≈ $1.50/month

### Performance Characteristics

| Limit | Value |
|---|---|
| Latency | **<100ms** for most operations |
| Writes per document | **1 write per second** limit (can burst) |
| Writes per collection | **10,000 writes/second** (soft limit, can be higher) |
| Collections and documents | Unlimited |
| Document size | 1 MB |
| Operations per transaction/batch | 500 |

### Use Cases
- **Mobile applications**: Chat apps, social networks, real-time collaboration
- **Web applications**: E-commerce, CMS, dashboards
- **Gaming**: Player profiles, leaderboards, game state
- **IoT**: Device data, telemetry (for small-medium scale)
- **Real-time updates**: Live sports scores, stock prices
- **Offline-first apps**: Field service, mobile forms

### When to Use Firestore
- Need real-time synchronization
- Mobile/web application with offline support
- **Serverless, pay-per-use model**
- Rich querying within collections
- Small to medium data volumes (<100 TB)
- Strong consistency required
- Rapid development with managed security

### When NOT to Use Firestore

| Need | Use instead |
|---|---|
| **Massive scale** (>100 TB) | [[gcp/bigtable|Bigtable]] |
| **Complex SQL queries** | [[gcp/cloud-sql|Cloud SQL]] or [[bigquery|BigQuery]] |
| **Analytics workloads** | [[bigquery|BigQuery]] |
| **Graph queries** | Specialized graph database |
| **High write throughput per document** (>1/sec sustained) | [[gcp/bigtable|Bigtable]] |
| **Full-text search** | Algolia or Elasticsearch (or export to BigQuery) |
| **Global strong consistency across regions** | [[cloud-spanner|Cloud Spanner]] |

### Integration with Other Services
#### Firebase
- **Native integration** with Firebase Authentication
- Firebase Cloud Messaging for push notifications
- Firebase Hosting for web apps
- Firebase Cloud Functions for serverless backend

#### Cloud Functions
```javascript
// Trigger on document write
exports.onUserCreate = functions.firestore
  .document('users/{userId}')
  .onCreate((snap, context) => {
    const newValue = snap.data();
    // Process new user
  });
```

#### BigQuery
- **Export Firestore to BigQuery** for analytics
- Streaming export (near real-time)
- Schedule exports with scheduled queries
- Query Firestore data with SQL

#### App Engine / Cloud Run
- Native client libraries
- Use service accounts for authentication

### Best Practices
#### Data Modeling
- **Denormalize data**: Store related data together (documents are cheap)
- **Avoid deep nesting**: Prefer sub-collections over deep maps
- **Use sub-collections** for one-to-many relationships
- **Keep documents small**: <1 MB, ideally <100 KB
- **Use document IDs wisely**: Sequential IDs = hotspots

#### Query Optimization
- Create necessary composite indexes
- Use query cursors for pagination
- Limit results (avoid fetching all documents)
- Use listeners sparingly (costs per snapshot)
- Cache data locally when possible

#### Security
- Always use security rules (never leave open)
- Validate data in rules, not just client-side
- Use Firebase Authentication for user identity
- Test rules with Rules Simulator
- Principle of least privilege

#### Performance
- Batch writes when possible (up to 500)
- Use transactions for atomic operations
- Avoid hotspots (sequential IDs, single document updates)
- Monitor usage in Firebase console
- Set up alerting for quota limits

---

## ACE Level

### Essential Firebase CLI Commands
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize project
firebase init firestore

# Deploy security rules
firebase deploy --only firestore:rules

# Deploy indexes
firebase deploy --only firestore:indexes

# Delete all data (emulator)
firebase firestore:delete --all-collections
```

### Essential gcloud Commands
```bash
# Create database (Native mode)
gcloud firestore databases create --region=us-east1

# Export data
gcloud firestore export gs://BUCKET_NAME

# Import data
gcloud firestore import gs://BUCKET_NAME/EXPORT_FOLDER

# List indexes
gcloud firestore indexes composite list

# Create index
gcloud firestore indexes composite create \
  --collection-group=COLLECTION \
  --query-scope=COLLECTION \
  --field-config field-path=FIELD1,order=ASCENDING \
  --field-config field-path=FIELD2,order=DESCENDING
```

### Client Library Examples
#### JavaScript (Web)
```javascript
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, addDoc, query, where, getDocs } from 'firebase/firestore';

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Add document
const docRef = await addDoc(collection(db, 'users'), {
  name: 'Alice',
  email: 'alice@example.com',
  age: 25
});

// Query
const q = query(collection(db, 'users'), where('age', '>', 18));
const querySnapshot = await getDocs(q);
querySnapshot.forEach((doc) => {
  console.log(doc.id, ' => ', doc.data());
});

// Real-time listener
onSnapshot(collection(db, 'users'), (snapshot) => {
  snapshot.forEach((doc) => {
    console.log(doc.data());
  });
});
```

#### Python (Server)
```python
from google.cloud import firestore

db = firestore.Client()

# Add document
doc_ref = db.collection('users').document('user123')
doc_ref.set({
    'name': 'Alice',
    'email': 'alice@example.com',
    'age': 25
})

# Query
users_ref = db.collection('users')
query = users_ref.where('age', '>', 18).limit(10)
docs = query.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')

# Transaction
@firestore.transactional
def update_counter(transaction, counter_ref):
    snapshot = counter_ref.get(transaction=transaction)
    count = snapshot.get('count')
    transaction.update(counter_ref, {'count': count + 1})

counter_ref = db.collection('counters').document('counter1')
transaction = db.transaction()
update_counter(transaction, counter_ref)
```

### Key Concepts for ACE
- Creating Firestore database (Native vs Datastore mode)
- Understanding document and collection structure
- Writing and reading documents
- Basic queries (where, orderBy, limit)
- Understanding security rules
- Creating composite indexes
- Using Firebase console for data management
- Exporting and importing data
- Monitoring usage and quotas

---

## PCA Level

### Data Modeling Strategies
#### Denormalization Pattern
```javascript
// GOOD: Denormalized (fast reads)
// User document
{
  userId: "user123",
  name: "Alice",
  email: "alice@example.com",
  recentOrders: [
    { orderId: "order1", total: 100, date: "2024-01-01" },
    { orderId: "order2", total: 50, date: "2024-01-05" }
  ]
}

// BAD: Normalized (requires multiple reads)
// User document
{ userId: "user123", name: "Alice", email: "alice@example.com" }
// Separate orders collection (need to query separately)
```

**Trade-off:** Storage cost vs read performance
- Denormalize for read-heavy workloads
- Keep documents under 1 MB
- Update duplicated data carefully

#### Sub-Collections Pattern
```javascript
// Parent-child relationship
users/{userId}/orders/{orderId}

// Allows:
// - Query all orders for a user
// - Scale to millions of orders
// - Organize data hierarchically
```

#### Collection Group Queries
```javascript
// Query all orders across all users
db.collectionGroup('orders')
  .where('status', '==', 'pending')
  .get();

// Requires collection group index
```

### Advanced Query Patterns
#### Pagination with Cursors
```javascript
// First page
const first = db.collection('products')
  .orderBy('name')
  .limit(25);

const snapshot = await first.get();
const lastVisible = snapshot.docs[snapshot.docs.length - 1];

// Next page
const next = db.collection('products')
  .orderBy('name')
  .startAfter(lastVisible)
  .limit(25);
```

#### Array Contains Queries
```javascript
// Find users with specific tag
db.collection('users')
  .where('tags', 'array-contains', 'premium')
  .get();

// Find users with any of multiple tags
db.collection('users')
  .where('tags', 'array-contains-any', ['premium', 'vip'])
  .get();
```

#### IN Queries
```javascript
// Find specific user IDs (up to 30 values)
db.collection('users')
  .where(documentId(), 'in', ['user1', 'user2', 'user3'])
  .get();
```

### Security Rules Patterns
#### Role-Based Access
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Helper function
    function isAdmin() {
      return get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }

    match /products/{productId} {
      allow read: if true;
      allow write: if isAdmin();
    }
  }
}
```

#### Field-Level Validation
```javascript
match /posts/{postId} {
  allow create: if request.resource.data.keys().hasAll(['title', 'content', 'author'])
                && request.resource.data.title is string
                && request.resource.data.title.size() >= 1
                && request.resource.data.title.size() <= 100
                && request.resource.data.author == request.auth.uid;

  allow update: if request.resource.data.diff(resource.data).affectedKeys().hasOnly(['content'])
                && request.auth.uid == resource.data.author;
}
```

### Performance Optimization
#### Avoiding Hotspots
```javascript
// BAD: Sequential document IDs (writes to same split)
db.collection('events').add({ timestamp: Date.now() });

// GOOD: Random IDs (distributed writes)
db.collection('events').doc().set({ timestamp: Date.now() });

// GOOD: Use server timestamp
db.collection('events').doc().set({
  timestamp: firebase.firestore.FieldValue.serverTimestamp()
});
```

#### Batching for Efficiency
```javascript
// Batch writes (atomic, efficient)
const batch = db.batch();

for (let i = 0; i < 500; i++) {
  const ref = db.collection('items').doc();
  batch.set(ref, { value: i });
}

await batch.commit();
```

#### Listener Optimization
```javascript
// BAD: Listen to entire collection
db.collection('messages').onSnapshot((snapshot) => {
  // Expensive if collection is large
});

// GOOD: Limit listener scope
db.collection('messages')
  .where('roomId', '==', currentRoom)
  .orderBy('timestamp', 'desc')
  .limit(50)
  .onSnapshot((snapshot) => {
    // Only recent messages in current room
  });
```

### Multi-Tenancy Strategies
#### Document-Level Tenancy
```javascript
// All tenants in same collection
db.collection('documents')
  .where('tenantId', '==', 'tenant123')
  .get();

// Pros: Simple, cost-effective
// Cons: Security rules complexity, potential data leakage
```

#### Collection-Level Tenancy
```javascript
// Separate collections per tenant
db.collection(`tenant_${tenantId}_documents`)
  .get();

// Pros: Better isolation
// Cons: Complex management, index overhead
```

#### Database-Level Tenancy
```javascript
// Separate Firestore databases per tenant (requires multiple projects)
// Pros: Complete isolation
// Cons: Highest cost, operational overhead
```

### Backup and Disaster Recovery
#### Scheduled Exports
```bash
# Use Cloud Scheduler + Cloud Functions
gcloud firestore export gs://backup-bucket/$(date +%Y%m%d)

# Retention policy on bucket
gsutil lifecycle set lifecycle.json gs://backup-bucket
```

#### Point-in-Time Recovery
- **No built-in PITR** (unlike Cloud SQL)
- Use scheduled exports for recovery
- Export to BigQuery for long-term retention
- Test restore procedures regularly

### Cost Optimization
#### Reduce Read Operations
```javascript
// Cache frequently accessed data locally
const cache = new Map();

async function getUser(userId) {
  if (cache.has(userId)) {
    return cache.get(userId);
  }

  const doc = await db.collection('users').doc(userId).get();
  cache.set(userId, doc.data());
  return doc.data();
}
```

#### Optimize Indexes
- Delete unused composite indexes
- Use single-field index exemptions for never-queried fields
- Monitor index storage in console

#### Storage Optimization
- Delete old documents (set TTL with Cloud Functions)
- Compress large strings
- Use Cloud Storage for files >1 MB

### Monitoring and Alerting
#### Key Metrics
- Document reads/writes/deletes per day
- Index entry counts
- Storage usage
- Security rule evaluation time
- Query performance

#### Alerting Setup
Cloud Monitoring alert policies:

| Alert | Threshold |
|---|---|
| Read operations | >80% of quota |
| Write operations | >80% of quota |
| Storage usage | >90% |
| Security rule evaluation time | High |

### Integration Patterns
#### Firestore + Cloud Functions (Event-Driven)
```javascript
// onCreate trigger
exports.onUserCreate = functions.firestore
  .document('users/{userId}')
  .onCreate(async (snap, context) => {
    // Send welcome email
    await sendEmail(snap.data().email);

    // Create default settings
    await db.collection('settings').doc(context.params.userId).set({
      theme: 'light',
      notifications: true
    });
  });

// onUpdate trigger
exports.onOrderUpdate = functions.firestore
  .document('orders/{orderId}')
  .onUpdate(async (change, context) => {
    const before = change.before.data();
    const after = change.after.data();

    if (before.status !** 'shipped' && after.status **= 'shipped') {
      // Order shipped, send notification
      await sendNotification(after.userId, 'Order shipped!');
    }
  });
```

#### Firestore + BigQuery (Analytics)
```javascript
// Set up BigQuery export (Console or CLI)
// Query Firestore data in BigQuery
SELECT
  document_name,
  JSON_EXTRACT_SCALAR(data, '$.name') as name,
  JSON_EXTRACT_SCALAR(data, '$.email') as email
FROM `project.dataset.users_raw_latest`
WHERE JSON_EXTRACT_SCALAR(data, '$.age') > '18';
```

#### Firestore + Full-Text Search
```javascript
// Option 1: Algolia integration
exports.onProductWrite = functions.firestore
  .document('products/{productId}')
  .onWrite(async (change, context) => {
    const algoliaIndex = algolia.initIndex('products');

    if (!change.after.exists) {
      // Delete from Algolia
      await algoliaIndex.deleteObject(context.params.productId);
    } else {
      // Update Algolia
      await algoliaIndex.saveObject({
        objectID: context.params.productId,
        ...change.after.data()
      });
    }
  });

// Option 2: BigQuery + Cloud Functions for search
```

### Advanced Security Patterns
#### Attribute-Based Access Control
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /documents/{docId} {
      allow read: if resource.data.visibility == 'public'
                  || (request.auth != null && resource.data.visibility == 'private'
                      && request.auth.uid == resource.data.ownerId)
                  || (request.auth != null && resource.data.visibility == 'shared'
                      && request.auth.uid in resource.data.sharedWith);
    }
  }
}
```

#### Rate Limiting with Security Rules
```javascript
// Not directly possible in security rules
// Implement with Cloud Functions + Firestore counters
match /api/{endpoint} {
  function rateLimitCheck() {
    let counter = get(/databases/$(database)/documents/rate_limits/$(request.auth.uid));
    return counter.data.count < 100;
  }

  allow read: if rateLimitCheck();
}
```

### Migration Strategies
#### From DynamoDB to Firestore
1. Export DynamoDB data to S3
2. Transfer to Cloud Storage
3. Use Dataflow to transform and load into Firestore
4. Update application code (SDK changes)
5. Update IAM/security rules

#### From MongoDB to Firestore
1. Export MongoDB collections
2. Transform to Firestore format (flatten nested objects, use sub-collections)
3. Import via Dataflow or batch writes
4. Redesign queries for Firestore limitations
5. Update application code

### Well-Architected Considerations
- **Operational Excellence**:
  - Automated backups via scheduled exports
  - Monitoring with Firebase/Cloud Monitoring
  - Infrastructure as Code (Terraform, Firebase CLI)
- **Reliability**:
  - Multi-region replication
  - Automatic scaling
  - Regular export testing
- **Security**:
  - Comprehensive security rules
  - Firebase Authentication integration
  - Audit logging
  - VPC Service Controls for sensitive data
- **Performance**:
  - Denormalization for read performance
  - Proper indexing strategy
  - Connection pooling for server apps
  - Offline support for mobile
- **Cost**:
  - Free tier for small apps
  - Caching to reduce reads
  - Index optimization
  - Delete old data
- **Sustainability**:
  - Serverless (no idle resources)
  - Efficient data modeling
  - Regional deployment when global not needed
