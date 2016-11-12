/****************************************************************************
**
** Copyright (C) 2016 Jolla Ltd.
** Contact: Bea Lam <bea.lam@jolla.com>
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 2.1 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU Lesser General Public License version 2.1 requirements
** will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**
****************************************************************************/

#include "obexagentadaptor_bluez4_p.h"
#include "obexmanager_bluez4_p.h"

#include "obexmanager.h"
#include "obextransfer.h"
#include "obexagent.h"
#include "utils.h"

#include <QDBusObjectPath>
#include <QDBusMessage>

namespace BluezQt
{

ObexAgentAdaptorBluez4::ObexAgentAdaptorBluez4(ObexAgent *parent, ObexManagerBluez4 *manager)
    : QDBusAbstractAdaptor(parent)
    , m_agent(parent)
    , m_manager(manager)
{
}

QString ObexAgentAdaptorBluez4::Authorize(const QDBusObjectPath &transfer, const QString &bt_address,
                                    const QString &name, const QString &type, qint32 length,
                                    qint32 time, const QDBusMessage &msg)
{
    // Set up the request as per ObexAgentAdaptor::AuthorizePush().
    msg.setDelayedReply(true);
    m_transferRequest = Request<QString>(OrgBluezObexAgent, msg);
    m_transferPath = transfer.path();

    m_transferRequest.setObjectPushTransferPath(transfer.path());

    // Assemble the map of property values. In BlueZ 4, transfer objects provided by the org.bluez.obex
    // service for OBEX agents (as opposed to those provided by the org.bluez.obex.client service
    // for OBEX clients) don't have persistent properties provided by a GetProperties() function;
    // instead, all values are provided by the AuthorizePush() arguments, so initialize them here.
    // Note 'Filename' is not added here as it not available in BlueZ 4 and is optional in BlueZ 5.
    QVariantMap properties;
    properties.insert(QStringLiteral("Status"), QStringLiteral("queued"));
    properties.insert(QStringLiteral("Name"), name);
    properties.insert(QStringLiteral("Type"), type);
    if (time > 0) {
        properties.insert(QStringLiteral("Time"), static_cast<quint64>(time));
    }
    if (length > 0) {
        properties.insert(QStringLiteral("Size"), static_cast<quint64>(length));
    }
    properties.insert(QStringLiteral("Transferred"), 0);

    QMetaObject::invokeMethod(this, "authorizeTransfer", Qt::QueuedConnection,
                              Q_ARG(QString, transfer.path()),
                              Q_ARG(QVariantMap, properties),
                              Q_ARG(QString, bt_address));

    return QString();
}

void ObexAgentAdaptorBluez4::Cancel()
{
    m_agent->cancel();
}

void ObexAgentAdaptorBluez4::Release()
{
    m_agent->release();
}

void ObexAgentAdaptorBluez4::authorizeTransfer(const QString &transferPath, const QVariantMap &transferProperties, const QString &destinationAddress)
{
    // For BlueZ 4 there is only FTP session support, so manually add per-transfer OPP sessions.
    ObexTransferPtr transfer = m_manager->newObjectPushTransfer(QDBusObjectPath(transferPath), transferProperties, destinationAddress);

    // Now pass the transfer to the agent, as per ObexAgentAdaptor::getPropertiesFinished().
    ObexSessionPtr session = m_manager->sessionForObjectPushTransfer(transfer->objectPath());
    Q_ASSERT(session);

    if (!session) {
        m_transferRequest.cancel();
        return;
    }

    m_agent->authorizePush(transfer, session, m_transferRequest);
}

} // namespace BluezQt